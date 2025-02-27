import os
import json
import argparse
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

from octotools.engine.openai import ChatOpenAI

@dataclass
class AnswerVerification:
    analysis: str
    true_false: bool

class ResultScorer:
    def __init__(self, llm_engine=None):
        self.llm_engine = llm_engine or ChatOpenAI(model_string="gpt-4o-mini", is_multimodal=False, enable_cache=True)
        print(f"\nLocal OpenAI engine {self.llm_engine.model_string} initialized.\n")

    def answer_verification(self, response: Dict[str, Any]) -> Tuple[str, bool]:
        """
        Verifies the structure and content of a Japanese proverb analysis response.
        
        Args:
            response: The model's response containing proverb and vocabulary analysis
            
        Returns:
            Tuple of (analysis string, boolean indicating if response is valid)
        """
        query_prompt = f"""
        This is a Japanese proverb analysis verification task. Verify that the response contains:
        1. A valid Japanese proverb
        2. Vocabulary analysis with required fields (kanji, reading, meaning, JLPT level)
        3. Accurate readings and translations
        
        Model response: {json.dumps(response, ensure_ascii=False, indent=2)}
        
        Response Format:
        <analysis>: Detailed analysis of the response validity
        <true_false>: Return "True" if response is valid, otherwise "False"
        """

        verification = self.llm_engine(query_prompt, response_format=AnswerVerification)
        
        analysis = verification.analysis.strip()
        true_false = verification.true_false

        return analysis, true_false

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_file', type=str, required=True)
    parser.add_argument('--result_dir', type=str, required=True)
    parser.add_argument('--response_type', type=str, default='direct_output')
    parser.add_argument('--output_file', type=str, default='final_results.json')
    args = parser.parse_args()

    # Initialize scorer
    scorer = ResultScorer()
    
    # Load results
    results_file = os.path.join(args.result_dir, f"output_0.json")
    if not os.path.exists(results_file):
        print(f"No results file found at {results_file}")
        return
        
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Get response based on response type
    response = results.get(args.response_type, {})
    
    # Verify response
    analysis, is_valid = scorer.answer_verification(response)
    
    # Save results
    output = {
        "valid_response": is_valid,
        "analysis": analysis,
        "response": response
    }
    
    output_path = os.path.join(args.result_dir, args.output_file)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
    print(f"\nResults saved to {output_path}")
    print(f"Valid response: {is_valid}")
    print(f"Analysis: {analysis}")

if __name__ == "__main__":
    main()