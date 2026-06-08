from typing import Optional
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


class PromptBuilder:
    SYSTEM_PROMPT = """You are a helpful and cautious AI medical assistant.
You only answer questions related to health, medicine, symptoms, diseases, and treatments.
If the question is not related to health or medicine, politely say:
'I can only answer health and medical related questions.'
If relevant medical context is provided below, prioritize it in your answer.
If no relevant context is provided, answer using your own medical knowledge.
You never give a definitive diagnosis.
Always recommend consulting a licensed doctor for personal medical advice.
Keep your answers clear, concise, and easy to understand."""

    def build(
        self,
        query: str,
        chunks: list,
        history: list,
        external_context: Optional[dict] = None,
    ) -> list:

        # handle empty chunks — let LLM answer on its own
        if not chunks:
            context_text = "No relevant documents found. Answer using your own medical knowledge."
        else:
            context_text = "\n\n".join([
                f"Source ({c.metadata.get('source', 'unknown')}):\n{c.page_content}"
                for c in chunks
            ])

        external_text = ""
        if external_context:
            if external_context.get("disease"):
                external_text += f"\nPredicted Disease: {external_context['disease']} (confidence: {external_context.get('confidence', 'N/A')})"
            if external_context.get("xray_result"):
                external_text += f"\nChest X-ray Result: {external_context['xray_result']}"
            if external_context.get("medicine"):
                external_text += f"\nRecommended Medicine: {external_context['medicine']}"

        system_content = f"""{self.SYSTEM_PROMPT}

--- Retrieved Medical Context ---
{context_text}
"""
        if external_text:
            system_content += f"\n--- Patient Module Results ---{external_text}\n"

        messages = [SystemMessage(content=system_content)]

        for turn in history:
            if turn["role"] == "user":
                messages.append(HumanMessage(content=turn["message"]))
            elif turn["role"] == "assistant":
                messages.append(AIMessage(content=turn["message"]))

        messages.append(HumanMessage(content=query))
        return messages