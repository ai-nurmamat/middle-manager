"""
Universal LLM Extractor for Chronos-MCP.

This module utilizes constrained JSON decoding to extract 4D Tuples (S-P-O-T)
from raw unstructured text, without requiring predefined schemas or ontologies.
"""

import json
import datetime
from typing import List, Dict, Any, Union
from openai import OpenAI

from .graph import UniversalHypergraph, FourDTuple, SourceEvidence


class UniversalExtractor:
    """
    A universal extractor that works with any OpenAI-compatible API
    (e.g., Minimax, DeepSeek, Anthropic via proxy).
    """

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        """
        Initialize the Universal Extractor.

        Args:
            api_key (str): The API key for the LLM service.
            base_url (str): The base URL of the OpenAI-compatible API.
            model (str): The model identifier to use (e.g., 'abab6.5-chat').
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def extract_to_graph(
        self,
        text: str,
        source_id: str,
        publish_date: datetime.datetime,
        graph: UniversalHypergraph,
    ) -> None:
        """
        Extract business and analytical facts from unstructured text and inject them
        directly into the Temporal Knowledge Graph.

        Args:
            text (str): The raw unstructured text (e.g., news article, financial report).
            source_id (str): A unique identifier for traceability.
            publish_date (datetime.datetime): The baseline publish date of the text.
            graph (UniversalHypergraph): The target hypergraph engine to inject data into.
        """
        prompt = f"""
        You are a world-class Temporal Knowledge Graph construction expert.
        Your task is to extract all commercially and analytically valuable facts from the text below, 
        and convert them into an array of 4D Tuples.
        
        【4D Tuple Rules (S, P, O, T)】:
        1. S (Subject): The main entity (e.g., company name, product, person). E.g., "Apple".
        2. P (Predicate): The property, relation, or action. NO PREDEFINED SCHEMA REQUIRED! Be creative but accurate. E.g., "gross margin", "invests in", "CEO".
        3. O (Object): The value or target entity. E.g., "28.5", "OpenAI", "Tim Cook".
        4. U (Unit): If the Object is numeric, extract its unit. E.g., "%", "Billion USD". Otherwise, leave empty.
        5. T (Time): The exact date this fact occurred or was valid (YYYY-MM-DD).
        6. Snippet: A short quote from the original text proving this fact.
        
        Baseline Time Context: The text was published on {publish_date.strftime('%Y-%m-%d')}.
        
        【STRICT REQUIREMENT】: Return ONLY a valid JSON array. No markdown blocks, no explanations.
        Format Example:
        [
          {{"S": "Apple", "P": "gross margin", "O": "45.2", "U": "%", "T": "2023-09-30", "Snippet": "Apple reported a gross margin of 45.2%"}},
          {{"S": "Apple", "P": "develops", "O": "Vision Pro", "U": "", "T": "2023-10-15", "Snippet": "started developing the Vision Pro"}}
        ]
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
                response_format={"type": "json_object"},
            )

            raw_content = response.choices[0].message.content or "{}"
            data = json.loads(raw_content)

            tuples: List[Dict[str, Any]] = []
            if isinstance(data, dict) and "tuples" in data:
                tuples = data["tuples"]
            elif isinstance(data, list):
                tuples = data
            else:
                # Attempt to extract from the first key if wrapped differently
                first_val = list(data.values())[0] if isinstance(data, dict) else []
                if isinstance(first_val, list):
                    tuples = first_val

            for t in tuples:
                evidence = SourceEvidence(
                    source_id=source_id,
                    text_snippet=t.get("Snippet", ""),
                    timestamp=publish_date,
                )

                # Robust time parsing
                time_str = t.get("T", publish_date.strftime("%Y-%m-%d"))
                try:
                    dt = datetime.datetime.strptime(time_str[:10], "%Y-%m-%d")
                except ValueError:
                    dt = publish_date

                tup = FourDTuple(
                    subject=t.get("S", ""),
                    predicate=t.get("P", ""),
                    object=str(t.get("O", "")),
                    time=dt,
                    unit=t.get("U", ""),
                    evidence=evidence,
                )
                graph.insert(tup)

            print(f"✅ Successfully extracted {len(tuples)} tuples from {source_id}.")

        except Exception as e:
            print(f"❌ Extraction failed for {source_id}: {e}")


class MockExtractor:
    """
    A mock extractor for local testing without requiring a real LLM API Key.
    Simulates the extraction of messy, schema-less data.
    """

    def extract_to_graph(
        self,
        text: str,
        source_id: str,
        publish_date: datetime.datetime,
        graph: UniversalHypergraph,
    ) -> None:
        """Simulate LLM extraction based on simple text matching."""
        if "2022" in text:
            tuples = [
                {
                    "S": "宁德时代",
                    "P": "毛利率",
                    "O": "27.0",
                    "U": "%",
                    "T": "2022-09-30",
                    "Snippet": "宁德时代毛利率为27.0%",
                },
                {
                    "S": "比亚迪",
                    "P": "储能毛利",
                    "O": "20.0",
                    "U": "%",
                    "T": "2022-09-30",
                    "Snippet": "比亚迪储能毛利率为20.0%",
                },
                {
                    "S": "宁王",
                    "P": "竞品",
                    "O": "比亚迪",
                    "U": "",
                    "T": "2022-10-15",
                    "Snippet": "宁王与比亚迪竞争加剧",
                },
            ]
        else:
            tuples = [
                {
                    "S": "CATL",
                    "P": "毛利",
                    "O": "28.5",
                    "U": "%",
                    "T": "2023-09-30",
                    "Snippet": "CATL毛利达到28.5%",
                },
                {
                    "S": "比亚迪",
                    "P": "储能毛利",
                    "O": "22.0",
                    "U": "%",
                    "T": "2023-09-30",
                    "Snippet": "比亚迪的储能毛利同期仅为22%",
                },
                {
                    "S": "CATL",
                    "P": "重仓",
                    "O": "全固态电池",
                    "U": "",
                    "T": "2023-10-15",
                    "Snippet": "CATL开始重仓全固态电池",
                },
            ]

        for t in tuples:
            evidence = SourceEvidence(
                source_id=source_id, text_snippet=t["Snippet"], timestamp=publish_date
            )
            dt = datetime.datetime.strptime(t["T"], "%Y-%m-%d")
            tup = FourDTuple(
                subject=t["S"],
                predicate=t["P"],
                object=t["O"],
                time=dt,
                unit=t["U"],
                evidence=evidence,
            )
            graph.insert(tup)

        print(f"✅ Mock Extracted {len(tuples)} tuples from {source_id}.")
