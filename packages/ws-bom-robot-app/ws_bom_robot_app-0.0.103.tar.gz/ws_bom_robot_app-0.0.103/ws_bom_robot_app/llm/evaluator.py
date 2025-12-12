from uuid import UUID
import requests, base64
from typing import Iterator, Optional, List, Union
from enum import Enum
from ws_bom_robot_app.config import config
from ws_bom_robot_app.llm.models.api import LlmMessage, StreamRequest
from langsmith import Client, traceable
from langsmith.schemas import Dataset, Example, Feedback, Run
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, RAG_HELPFULNESS_PROMPT, CONCISENESS_PROMPT, RAG_GROUNDEDNESS_PROMPT, HALLUCINATION_PROMPT
from pydantic import BaseModel

ls_client = Client()

class EvaluatorType(Enum):
    """Available evaluator types"""
    CORRECTNESS = "correctness"
    HELPFULNESS = "helpfulness"
    CONCISENESS = "conciseness"
    RAG_GROUNDEDNESS = "rag_groundedness"
    RAG_HALLUCINATION = "rag_hallucination"

    @classmethod
    def all(cls) -> List['EvaluatorType']:
        """Get all available evaluator types"""
        return list(cls)

    @classmethod
    def default(cls) -> List['EvaluatorType']:
        """Get default evaluator types"""
        return [cls.CORRECTNESS]

class EvaluatorDataSets:

    @classmethod
    def all(cls) -> List[Dataset]:
        return list(ls_client.list_datasets())
    @classmethod
    def find(cls, name: str) -> List[Dataset]:
        return [d for d in cls.all() if d.name.lower().__contains__(name.lower())]
    @classmethod
    def get(cls, id: Union[str, UUID]) -> Optional[Dataset]:
        return next((d for d in cls.all() if str(d.id) == str(id)), None)
    @classmethod
    def create(cls, name: str) -> Dataset:
        return ls_client.create_dataset(name=name)
    @classmethod
    def delete(cls, id: str) -> None:
        ls_client.delete_dataset(id=id)
    @classmethod
    def example(cls, id: str) -> List[Example]:
        return list(ls_client.list_examples(dataset_id=id, include_attachments=True))
    @classmethod
    def add_example(cls, dataset_id: str, inputs: dict, outputs: dict) -> Example:
        """Add an example to the dataset.
        Args:
            inputs (dict): The input data for the example.
            outputs (dict): The output data for the example.
        Sample:
            - inputs: {"question": "What is the capital of France?"}
              outputs: {"answer": "Paris"}
        """
        return ls_client.create_example(dataset_id=dataset_id, inputs=inputs, outputs=outputs)
    @classmethod
    def feedback(cls, experiment_name: str) -> Iterator[Feedback]:
        return ls_client.list_feedback(
            run_ids=[r.id for r in ls_client.list_runs(project_name=experiment_name)]
        )

class Evaluator:
    def __init__(self, rq: StreamRequest, data: Union[Dataset,List[Example]], judge_model: Optional[str] = None):
        """Evaluator class for assessing model performance.

        Args:
            rq (StreamRequest): The request object containing input data.
            data (Union[Dataset, List[Example]]): The dataset to use for evaluation or a list of examples.
            judge_model (Optional[str], optional): The model to use for evaluation, defaults to "openai:o4-mini".
              For a list of available models, see the LangChain documentation:
              https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html
        """
        self.judge_model: str = judge_model or "openai:o4-mini"
        self.data = data
        self.rq: StreamRequest = rq

    #region evaluators

    def _get_evaluator_function(self, evaluator_type: EvaluatorType):
        """Get the evaluator function for a given type"""
        evaluator_map = {
            EvaluatorType.CORRECTNESS: self.correctness_evaluator,
            EvaluatorType.HELPFULNESS: self.helpfulness_evaluator,
            EvaluatorType.CONCISENESS: self.conciseness_evaluator,
            EvaluatorType.RAG_GROUNDEDNESS: self.rag_groundedness_evaluator,
            EvaluatorType.RAG_HALLUCINATION: self.rag_hallucination_evaluator,
        }
        return evaluator_map.get(evaluator_type)

    def correctness_evaluator(self, inputs: dict, outputs: dict, reference_outputs: dict):
        evaluator = create_llm_as_judge(
          prompt=CORRECTNESS_PROMPT,
          feedback_key="correctness",
          model=self.judge_model,
          continuous=True,
          choices=[i/10 for i in range(11)]
        )
        return evaluator(
            inputs=inputs,
            outputs=outputs,
            reference_outputs=reference_outputs
        )

    def helpfulness_evaluator(self, inputs: dict, outputs: dict):
        evaluator = create_llm_as_judge(
            prompt=RAG_HELPFULNESS_PROMPT,
            feedback_key="helpfulness",
            model=self.judge_model,
            continuous=True,
            choices=[i/10 for i in range(11)]
        )
        return evaluator(
            inputs=inputs,
            outputs=outputs,
        )

    def conciseness_evaluator(self, inputs: dict, outputs: dict, reference_outputs: dict):
        evaluator = create_llm_as_judge(
            prompt=CONCISENESS_PROMPT,
            feedback_key="conciseness",
            model=self.judge_model,
            continuous=True,
            choices=[i/10 for i in range(11)]
        )
        return evaluator(
            inputs=inputs,
            outputs=outputs,
            reference_outputs=reference_outputs
        )

    def _find_retrievers(self, run: Run) -> List[Run]:
      retrievers = []
      for child in getattr(run, "child_runs", []):
        if child.run_type == "retriever":
          retrievers.append(child)
        retrievers.extend(self._find_retrievers(child))
      return retrievers

    def _retriever_documents(self, retrievers_run: List[Run]) -> str:
      unique_contents = set()
      for r in retrievers_run:
        for doc in r.outputs.get("documents", []):
          unique_contents.add(doc.page_content)
      return "\n\n".join(unique_contents)

    def rag_groundedness_evaluator(self, run: Run):
        evaluator = create_llm_as_judge(
            prompt=RAG_GROUNDEDNESS_PROMPT,
            feedback_key="rag_groundedness",
            model=self.judge_model,
            continuous=True,
            choices=[i/10 for i in range(11)]
        )
        retrievers_run = self._find_retrievers(run)
        if retrievers_run:
            try:
                return evaluator(
                    outputs=run.outputs["answer"],
                    context=self._retriever_documents(retrievers_run)
                )
            except Exception as e:
                return 0.0
        else:
            return 0.0

    def rag_hallucination_evaluator(self, inputs: dict, outputs: dict, reference_outputs: dict, run: Run):
        evaluator = create_llm_as_judge(
            prompt=HALLUCINATION_PROMPT,
            feedback_key="rag_hallucination",
            model=self.judge_model,
            continuous=True,
            choices=[i/10 for i in range(11)]
        )
        retrievers_run = self._find_retrievers(run)
        if retrievers_run:
            try:
                return evaluator(
                    inputs=inputs['question'],
                    outputs=outputs['answer'],
                    reference_outputs=reference_outputs['answer'],
                    context=self._retriever_documents(retrievers_run)
                )
            except Exception as e:
                return 0.0
        else:
            return 0.0

    #endregion evaluators

    #region target
    def _parse_rq(self, inputs: dict, attachments: dict) -> StreamRequest:
        _rq = self.rq.__deepcopy__()
        if not attachments is None and len(attachments) > 0:
            _content = []
            _content.append({"type": "text", "text": inputs["question"]})
            for k,v in attachments.items():
                if isinstance(v, dict):
                    _content.append({"type": ("image" if "image" in v.get("mime_type","") else "file"), "url": v.get("presigned_url","")})
            _rq.messages = [LlmMessage(role="user", content=_content)]
        else:
            _rq.messages = [LlmMessage(role="user", content=inputs["question"])]
        return _rq

    @traceable(run_type="chain",name="stream_internal")
    async def target_internal(self,inputs: dict, attachments: dict) -> dict:
      from ws_bom_robot_app.llm.main import stream
      from unittest.mock import Mock
      from fastapi import Request
      _ctx = Mock(spec=Request)
      _ctx.base_url.return_value = "http://evaluator"
      _rq = self._parse_rq(inputs, attachments)
      _chunks = []
      async for chunk in stream(rq=_rq, ctx=_ctx, formatted=False):
          _chunks.append(chunk)
      _content = ''.join(_chunks) if _chunks else ""
      del _rq, _chunks
      return { "answer": _content.strip() }

    @traceable(run_type="chain",name="stream_http")
    async def target_http(self,inputs: dict, attachments: dict) -> dict:
      _rq = self._parse_rq(inputs, attachments)
      _host= "http://localhost:6001"
      _endpoint = f"{_host}/api/llm/stream/raw"
      _robot_auth =f"Basic {base64.b64encode((config.robot_user + ':' + config.robot_password).encode('utf-8')).decode('utf-8')}"
      _rs = requests.post(_endpoint, data=_rq.model_dump_json(), stream=True, headers={"Authorization": _robot_auth}, verify=True)
      _content = ''.join([chunk.decode('utf-8') for chunk in _rs.iter_content(chunk_size=1024, decode_unicode=False)])
      del _rq, _rs
      return { "answer": _content.strip() }
    #endregion target

    async def run(self,
                  evaluators: Optional[List[EvaluatorType]] = None,
                  target_method: str = "target_internal") -> dict:
        """Run evaluation with specified evaluators

        Args:
            evaluators: List of evaluator types to use. If None, uses default (correctness only)
            target_method: Method to use for target evaluation ("target_internal" or "target")

        Returns:
            dict: Evaluation results with scores

        Usage:
          ```
          await evaluator.run()  # Uses default (correctness only)
          await evaluator.run([EvaluatorType.CORRECTNESS, EvaluatorType.HELPFULNESS])
          await evaluator.run(EvaluatorType.all())  # Uses all available evaluators
          ```
        """
        try:
          # evaluator functions
          evaluator_functions = []
          if evaluators is None:
              evaluators = EvaluatorType.default()
          for eval_type in evaluators:
              func = self._get_evaluator_function(eval_type)
              if func:
                  evaluator_functions.append(func)
              else:
                  print(f"Warning: Unknown evaluator type: {eval_type}")
          if not evaluator_functions:
              print("No valid evaluators provided, using default (correctness)")
              evaluator_functions = [self.correctness_evaluator]

          # target method
          target_func = getattr(self, target_method, self.target_internal)

          # run
          _dataset: Dataset = self.data if isinstance(self.data, Dataset) else EvaluatorDataSets.get(self.data[0].dataset_id)
          experiment = await ls_client.aevaluate(
              target_func,
              data=_dataset.name if isinstance(self.data, Dataset) else self.data,
              evaluators=evaluator_functions,
              experiment_prefix=_dataset.name,
              upload_results=True,
              max_concurrency=4,
              metadata={
                  "app": _dataset.name,
                  "model": f"{self.rq.provider}:{self.rq.model}",
                  "judge": self.judge_model,
                  "evaluators": [e.value for e in evaluators]
              }
          )
          feedback = list(EvaluatorDataSets.feedback(experiment.experiment_name))
          scores = [f.score for f in feedback]
          url = f"{ls_client._host_url}/o/{ls_client._tenant_id}/datasets/{_dataset.id}/compare?selectedSessions={feedback[0].session_id}"

          # group scores by evaluator type
          evaluator_scores = {}
          for i, eval_type in enumerate(evaluators):
              eval_scores = [f.score for f in feedback if f.key.lower() == eval_type.value.lower()]
              if eval_scores:
                  evaluator_scores[eval_type.value] = sum(eval_scores) / len(eval_scores)

          return {
              "experiment": {"name": experiment.experiment_name, "url": url},
              "overall_score": sum(scores) / len(scores) if scores else 0,
              "evaluator_scores": evaluator_scores
          }
        except Exception as e:
            from traceback import print_exc
            print(f"Error occurred during evaluation: {e}")
            print_exc()
            return {"error": str(e)}

class EvaluatorRunRequest(BaseModel):
    dataset: dict
    rq: StreamRequest
    example: Optional[List[dict]] = None
    evaluators: Optional[List[str]] = None
    judge: Optional[str] = None
