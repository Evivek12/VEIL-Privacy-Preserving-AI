
import streamlit as st

from profiler import profile_query
from router import choose_route
from prompt_creator import create_safe_prompt
from verifier import verify_prompt
from aggregator import get_final_answer


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="VEIL Privacy Assistant",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ VEIL – Privacy-Preserving AI Assistant")

st.caption(
    "Verified, Intent-Preserving Delegation between "
    "Local and Remote Language Models"
)

st.success(
    "Local AI Mode Active: Using Llama 3.2 through Ollama. "
    "No remote AI service is connected."
)


# --------------------------------------------------
# 2. USER INPUT
# --------------------------------------------------

query = st.text_area(
    "Enter your query",
    height=150,
    placeholder=(
        "Example: My name is Alex Kumar and my phone "
        "number is 9876543210. Draft an internship email."
    )
)

run = st.button(
    "Analyze and process query",
    type="primary",
    disabled=not query.strip()
)


# --------------------------------------------------
# 3. VEIL PROCESSING PIPELINE
# --------------------------------------------------

if run:

    with st.spinner("VEIL is analyzing your query..."):

        # Step 1: Query profiling
        profile = profile_query(query)

        # Step 2: Routing decision
        route = choose_route(profile)

        # Step 3: Prompt sanitization
        safe_prompt = create_safe_prompt(
            query,
            profile
        )

        # Step 4: Verification
        verification = verify_prompt(
            query,
            safe_prompt,
            profile
        )

    # --------------------------------------------------
    # 4. QUERY PROFILE
    # --------------------------------------------------

    st.divider()
    st.header("1. Query Profile")

    c1, c2 = st.columns(2)

    with c1:
        st.write("**Task Type:**", profile["task_type"])

        st.write("**Detected Private Information:**")

        if profile["pii"]:

            for item in profile["pii"]:
                st.write(
                    f"- {item['type']}: `{item['value']}`"
                )

        else:
            st.write("No supported PII pattern detected.")

        st.write("**Total PII Detected:**", len(profile["pii"]))

    with c2:
        st.write("**Original Query Length:**",
                 profile["query_length"])

        st.write("**PII Detection Status:**")

        if profile["pii"]:
            st.success("Private information detected")
        else:
            st.info("No supported PII detected")

    # --------------------------------------------------
    # 5. ROUTING DECISION
    # --------------------------------------------------

    st.divider()
    st.header("2. Routing Decision")

    st.write("**Policy Decision:**", route["route"])
    st.write(route["reason"])

    st.info(
        "Execution mode: Local Ollama model. "
        "Remote delegation is not implemented yet."
    )

    # --------------------------------------------------
    # 6. PROMPT SANITIZATION
    # --------------------------------------------------

    st.divider()
    st.header("3. Privacy-Preserving Prompt")

    st.write("Personal information is replaced with placeholders.")

    st.code(
        safe_prompt,
        language="text"
    )

    # --------------------------------------------------
    # 7. VERIFICATION GATE
    # --------------------------------------------------

    st.divider()
    st.header("4. Verification Gate")

    if verification["passed"]:

        st.success("Verification Passed")

    else:

        st.error(
            "Verification Failed – AI processing blocked."
        )

    st.write(
        "**Intent Check:**",
        verification["intent"]
    )

    st.write(
        "**Leakage Check:**",
        verification["leakage"]
    )

    st.write(
        "**Well-formedness:**",
        verification["well_formed"]
    )

    # --------------------------------------------------
    # 8. LOCAL AI MODEL
    # --------------------------------------------------

    st.divider()
    st.header("5. Local AI Response")

    local_model_used = False
    answer = ""

    if verification["passed"]:

        try:

            with st.spinner(
                "Llama 3.2 is generating your answer..."
            ):

                answer = get_final_answer(
                    query,
                    safe_prompt,
                    route="LOCAL_OLLAMA"
                )

            local_model_used = True

            st.success(
                "Local Llama 3.2 processing completed."
            )

            st.write(answer)

        except Exception as error:

            st.error(
                f"Local AI processing failed: {error}"
            )

            st.info(
                "Check whether Ollama is running and "
                "llama3.2:3b is installed."
            )

    else:

        st.warning(
            "The verification gate blocked AI processing."
        )

    # --------------------------------------------------
    # 9. EVALUATION RECORD
    # --------------------------------------------------

    st.divider()
    st.header("6. Evaluation Record")

    evaluation = {
        "task_type": profile["task_type"],
        "pii_count": len(profile["pii"]),
        "routing_decision": route["route"],
        "verification_passed": verification["passed"],
        "local_model_requested": local_model_used,
        "model": "llama3.2:3b",
        "remote_call_made": False
    }

    st.json(evaluation)

    # --------------------------------------------------
    # 10. PRIVACY NOTICE
    # --------------------------------------------------

    st.caption(
        "VEIL Prototype: PII detection uses basic regular "
        "expressions and heuristic checks. These checks "
        "do not guarantee complete privacy protection. "
        "No remote AI API is connected in this version."
    )
