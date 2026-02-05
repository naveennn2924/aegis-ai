import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))


import streamlit as st
from storage.review_repo import get_items_for_review, save_review

st.set_page_config(page_title="AegisAI Review Dashboard")

st.title("🛡️ AegisAI – Human Review Dashboard")

items = get_items_for_review()

if not items:
    st.success("No items require review 🎉")
else:
    for item in items:
        st.divider()
        st.write(f"### Trace ID: `{item['trace_id']}`")

        result = item["result"]
        st.json(result)

        decision = st.radio(
            "Decision",
            ["approve", "reject"],
            key=item["trace_id"]
        )

        comment = st.text_input(
            "Reviewer comment",
            key=f"comment_{item['trace_id']}"
        )

        if st.button("Submit Review", key=f"submit_{item['trace_id']}"):
            save_review(item["trace_id"], decision, comment)
            st.success("Review saved ✔")
