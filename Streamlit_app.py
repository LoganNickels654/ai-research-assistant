#!/usr/bin/env python3
"""
Streamlit Web Interface for Research Assistant
Simple web app where students can input questions and get results
"""

import streamlit as st
import asyncio
from research_assistant import ResearchAssistant
import time

# Configure the page
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# Initialize the research assistant
@st.cache_resource
def get_research_assistant():
    return ResearchAssistant()

async def search_papers(question, max_papers):
    """Async function to search for papers"""
    assistant = get_research_assistant()
    return await assistant.process_research_question(question, max_papers)

def run_search(question, max_papers):
    """Run the async search function"""
    return asyncio.run(search_papers(question, max_papers))

# Main app interface
def main():
    st.title("Academic Research Assistant")
    st.write("Enter your research question and get relevant academic papers from PubMed")
    
    # Input form
    with st.form("search_form"):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            question = st.text_input(
                "Research Question:",
                placeholder="How does exercise affect depression in adults?",
                help="Enter your research question in natural language"
            )
        
        with col2:
            max_papers = st.selectbox(
                "Max Papers:",
                options=[3, 5, 10, 15],
                index=1,
                help="Number of papers to return"
            )
        
        submitted = st.form_submit_button("Search Papers", type="primary")
    
    # Process the search
    if submitted and question:
        with st.spinner("Searching PubMed and analyzing papers..."):
            try:
                # Record start time
                start_time = time.time()
                
                # Run the search
                results = run_search(question, max_papers)
                
                # Calculate time taken
                time_taken = time.time() - start_time
                
                if results:
                    # Display results summary
                    st.success(f"Found {len(results)} relevant papers in {time_taken:.1f} seconds")
                    
                    # Display each paper
                    for i, paper in enumerate(results, 1):
                        with st.expander(f"{i}. {paper.title}", expanded=(i <= 3)):
                            # Paper details
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**Authors:** {', '.join(paper.authors[:5])}")
                                st.write(f"**Journal:** {paper.journal} ({paper.year})")
                                
                            with col2:
                                # Relevance score with color coding
                                score = paper.relevance_score
                                if score >= 8:
                                    st.success(f"Relevance: {score}/10")
                                elif score >= 6:
                                    st.warning(f"Relevance: {score}/10")
                                else:
                                    st.info(f"Relevance: {score}/10")
                            
                            # Relevance reason
                            st.write(f"**Why relevant:** {paper.relevance_reason}")
                            
                            # Abstract
                            st.write(f"**Abstract:** {paper.abstract}")
                            
                            # PubMed link
                            st.markdown(f"[📖 View on PubMed]({paper.pubmed_url})")
                            
                            st.divider()
                
                else:
                    st.warning("No papers found. Try rephrasing your question or using different keywords.")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.write("Please check your API keys and try again.")
    
    elif submitted and not question:
        st.warning("Please enter a research question!")
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("How to Use")
        st.write("""
        1. **Enter your research question** in natural language
        2. **Choose how many papers** you want to see
        3. **Click 'Search Papers'** and wait for results
        4. **Click on each paper** to see full details
        5. **Visit PubMed links** for complete articles
        """)
        
        st.header("Example Questions")
        example_questions = [
            "How does exercise affect depression?",
            "What are the benefits of meditation?",
            "Does caffeine improve athletic performance?",
            "How does screen time affect children?",
            "What causes burnout in nurses?"
        ]
        
        for example in example_questions:
            if st.button(example, key=example):
                st.rerun()
        
        st.header("About")
        st.write("""
        This tool uses AI to:
        - Convert your question to medical search terms
        - Find relevant papers in PubMed
        - Rank results by relevance to your question
        
        Built with Streamlit and Claude AI.
        """)

if __name__ == "__main__":
    main()