"""
Lesson 3 — Streaming, Async & Batch Execution
==============================================

Complete implementation for Lesson 3 of the LangChain roadmap.

Covers:
    - invoke()
    - stream()
    - ainvoke()
    - astream()
    - batch()
    - abatch()
    - RunnableParallel vs batch()
    - TTFT and total-latency measurement
    - Basic async concurrency

Requirements:
    pip install -U langchain langchain-core langchain-ollama

Ollama:
    ollama pull qwen3:8b

Run:
    python 06_execution_modes.py
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_ollama import ChatOllama


MODEL_NAME = "qwen3:8b"
TEMPERATURE = 0

QUESTIONS = [
    {"topic": "LangChain"},
    {"topic": "RAG"},
    {"topic": "LangGraph"},
]


@dataclass
class TimingResult:
    first_output_ms: float | None
    total_ms: float


def elapsed_ms(start: float) -> float:
    return (time.perf_counter() - start) * 1000


def build_chain():
    """Build: input -> prompt -> Qwen3 -> string parser."""

    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a senior AI engineer teaching LangChain. "
                "Be concise and technically accurate.",
            ),
            (
                "human",
                "Explain {topic} in 3 short sentences.",
            ),
        ]
    )

    parser = StrOutputParser()

    return prompt | llm | parser


def demo_invoke(chain) -> TimingResult:
    """Synchronous, single complete execution."""

    print("\n" + "=" * 70)
    print("1. invoke() — synchronous complete execution")
    print("=" * 70)

    start = time.perf_counter()

    result = chain.invoke({"topic": "LangChain"})

    total_ms = elapsed_ms(start)

    print("\nResult:")
    print(result)
    print(f"\nTotal latency: {total_ms:.2f} ms")

    return TimingResult(None, total_ms)


def demo_stream(chain) -> TimingResult:
    """Synchronous streaming with TTFT measurement."""

    print("\n" + "=" * 70)
    print("2. stream() — synchronous streaming")
    print("=" * 70)

    start = time.perf_counter()
    first_output_ms = None

    print("\nStreaming response:")
    print("-" * 70)

    for chunk in chain.stream({"topic": "RAG"}):
        if first_output_ms is None:
            first_output_ms = elapsed_ms(start)

        print(chunk, end="", flush=True)

    total_ms = elapsed_ms(start)

    print("\n" + "-" * 70)
    print(f"TTFT: {first_output_ms:.2f} ms")
    print(f"Total latency: {total_ms:.2f} ms")

    return TimingResult(first_output_ms, total_ms)


async def demo_ainvoke(chain) -> TimingResult:
    """Asynchronous, single complete execution."""

    print("\n" + "=" * 70)
    print("3. ainvoke() — asynchronous complete execution")
    print("=" * 70)

    start = time.perf_counter()

    result = await chain.ainvoke({"topic": "LangGraph"})

    total_ms = elapsed_ms(start)

    print("\nResult:")
    print(result)
    print(f"\nTotal latency: {total_ms:.2f} ms")

    return TimingResult(None, total_ms)


async def demo_astream(chain) -> TimingResult:
    """Asynchronous streaming with TTFT measurement."""

    print("\n" + "=" * 70)
    print("4. astream() — asynchronous streaming")
    print("=" * 70)

    start = time.perf_counter()
    first_output_ms = None

    print("\nStreaming response:")
    print("-" * 70)

    async for chunk in chain.astream({"topic": "Agentic AI"}):
        if first_output_ms is None:
            first_output_ms = elapsed_ms(start)

        print(chunk, end="", flush=True)

    total_ms = elapsed_ms(start)

    print("\n" + "-" * 70)
    print(f"TTFT: {first_output_ms:.2f} ms")
    print(f"Total latency: {total_ms:.2f} ms")

    return TimingResult(first_output_ms, total_ms)


def demo_batch(chain) -> list[Any]:
    """Run the same Runnable against multiple inputs."""

    print("\n" + "=" * 70)
    print("5. batch() — multiple inputs")
    print("=" * 70)

    start = time.perf_counter()

    results = chain.batch(QUESTIONS)

    total_ms = elapsed_ms(start)

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}:")
        print(result)

    print(f"\nTotal batch latency: {total_ms:.2f} ms")

    return results


async def demo_abatch(chain) -> list[Any]:
    """Asynchronous batch execution."""

    print("\n" + "=" * 70)
    print("6. abatch() — asynchronous batch")
    print("=" * 70)

    start = time.perf_counter()

    results = await chain.abatch(QUESTIONS)

    total_ms = elapsed_ms(start)

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}:")
        print(result)

    print(f"\nTotal async batch latency: {total_ms:.2f} ms")

    return results


def demo_runnable_parallel() -> None:
    """
    Show the difference between RunnableParallel and batch().

    RunnableParallel:
        one input -> multiple branches

    batch():
        multiple inputs -> same Runnable
    """

    print("\n" + "=" * 70)
    print("7. RunnableParallel vs batch()")
    print("=" * 70)

    parallel = RunnableParallel(
        question=RunnablePassthrough(),
        length=lambda text: len(text),
        uppercase=lambda text: text.upper(),
    )

    result = parallel.invoke("What is RAG?")

    print("\nRunnableParallel result:")
    print(result)

    print(
        """
Concept:

RunnableParallel
-----------------
                  ┌──> question
Input ────────────┼──> length
                  └──> uppercase

batch()
-------
Input 1 ──> Chain ──> Output 1
Input 2 ──> Chain ──> Output 2
Input 3 ──> Chain ──> Output 3
"""
    )


async def run_one(chain, topic: str) -> tuple[str, float]:
    """Run one asynchronous request and return its result and latency."""

    start = time.perf_counter()

    result = await chain.ainvoke({"topic": topic})

    return result, elapsed_ms(start)


async def demo_concurrency(chain) -> None:
    """Run several async requests concurrently."""

    print("\n" + "=" * 70)
    print("8. Async concurrency experiment")
    print("=" * 70)

    topics = ["LangChain", "RAG", "LangGraph"]

    start = time.perf_counter()

    results = await asyncio.gather(
        *(run_one(chain, topic) for topic in topics)
    )

    total_ms = elapsed_ms(start)

    for topic, (result, latency) in zip(topics, results):
        print(f"\n[{topic}]")
        print(f"Individual latency: {latency:.2f} ms")
        print(result)

    print(f"\nConcurrent total time: {total_ms:.2f} ms")

    print(
        """
Measure before choosing a concurrency limit:
    - TTFT
    - total latency
    - tokens/sec
    - GPU utilization
    - VRAM
    - RAM
    - throughput
"""
    )


def print_summary(
    invoke_result: TimingResult,
    stream_result: TimingResult,
    ainvoke_result: TimingResult,
    astream_result: TimingResult,
) -> None:
    """Print execution-mode comparison."""

    print("\n" + "=" * 70)
    print("EXECUTION MODE SUMMARY")
    print("=" * 70)

    rows = [
        ("invoke()", None, invoke_result.total_ms, "Sync + complete"),
        ("stream()", stream_result.first_output_ms, stream_result.total_ms, "Sync + streaming"),
        ("ainvoke()", None, ainvoke_result.total_ms, "Async + complete"),
        ("astream()", astream_result.first_output_ms, astream_result.total_ms, "Async + streaming"),
    ]

    print(f"{'Method':<12}{'TTFT (ms)':<15}{'Total (ms)':<15}Description")
    print("-" * 70)

    for method, ttft, total, description in rows:
        ttft_text = f"{ttft:.2f}" if isinstance(ttft, float) else "-"
        print(f"{method:<12}{ttft_text:<15}{total:<15.2f}{description}")


async def main() -> None:
    """Run every Lesson 3 demonstration."""

    print("=" * 70)
    print("LESSON 3 — STREAMING, ASYNC & BATCH EXECUTION")
    print("=" * 70)
    print(f"Model: {MODEL_NAME}")
    print(f"Temperature: {TEMPERATURE}")

    chain = build_chain()

    invoke_result = demo_invoke(chain)
    stream_result = demo_stream(chain)

    ainvoke_result = await demo_ainvoke(chain)
    astream_result = await demo_astream(chain)

    demo_batch(chain)
    await demo_abatch(chain)

    demo_runnable_parallel()
    await demo_concurrency(chain)

    print_summary(
        invoke_result,
        stream_result,
        ainvoke_result,
        astream_result,
    )

    print("\nComplete.")


if __name__ == "__main__":
    asyncio.run(main())
