import streamlit as st
import pandas as pd
import plotly.express as px

# --- Mobile-friendly settings ---
st.set_page_config(page_title="AI Persona Voting", page_icon="🤖", layout="centered")

# CSS to make everything look good on mobile devices
# CSS to make everything look good on mobile devices
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    .persona-box { 
        padding: 20px; 
        border-radius: 10px; 
        background-color: #f0f2f6; 
        color: #1A1A1A !important; /* AICI E REZOLVAREA: Forțează textul închis la culoare */
        margin-bottom: 20px; 
        border-left: 5px solid #ff4b4b; 
    }
    </style>
""", unsafe_allow_html=True)

# --- LOCAL DATABASE (In-Memory for the session) ---
# This function keeps the votes active across all users during your presentation.
@st.cache_resource
def get_vote_tally():
    return {k: 0 for k in PERSONAS_DATA.keys()}

# --- FULL PERSONA DATASET ---
PERSONAS_DATA = {
    "Strict Manager 👔": {
        "text": "**Bad**\n\n* Food not cooked fresh in some cases (reheated).\n* Long wait times (10 mins for drinks, 45 mins for dessert pizza).\n* Dreadful and unfriendly service.\n\n**Good**\n\n* Freshness and quality praised by many.\n* Good variety of options.\n* Cozy and adorable atmosphere.\n\n**Manager Satisfaction Score: 6/10**",
        "accuracy": "4/5",
        "actionability": "3/5",
        "feedback": "Mostly accurate, but slightly intensifies the tone. Provides some actionable insights, but stops short of concrete recommendations."
    },
    "Culinary Expert 🧑‍🍳": {
        "text": "**Main Flavor Profiles:** Asian-inspired dishes (sushi) are a highlight. Italian dishes (lasagna) well-received. Desserts are a hit.\n\n**Strengths:** Fresh ingredients, generous portions, creative desserts.\n\n**Weaknesses:** Reheated food, overcooked/underseasoned dishes (steaks), uneventful menu.\n\n**Overall Culinary Score: 7.5/10**",
        "accuracy": "3/5",
        "actionability": "3/5",
        "feedback": "Partially accurate. Does not invent new entities but slightly reframes data. Lacks specific operational issues."
    },
    "Data Analyst 📊": {
        "text": "**Top Mentioned Food Items:**\n1. Sushi (14 mentions) - Positive\n2. Desserts (8 mentions) - Positive\n3. Lasagna (4 mentions) - Positive\n4. Steak (3 mentions) - Negative\n\n**Operational Food Score: 8.2/10**\nOverall high satisfaction, but negative sentiment towards steak and pizza suggest quality control areas.",
        "accuracy": "5/5",
        "actionability": "4/5",
        "feedback": "Accurately captures sentiment analysis without inventing entities. Stops just short of concrete recommendations."
    },
    "Gordon Ramsay 🍳": {
        "text": "**Disaster Score: 8/10**\n\nThe restaurant's food quality is a disaster! Overreliance on reheated dishes, two wasted steaks (what a crime!), and lack of seasoning. 45 minutes for a dessert pizza?! Shut it down and retrain your staff! Immediate improvements are necessary to salvage this reputation.",
        "accuracy": "3/5",
        "actionability": "2/5",
        "feedback": "Invents specific entities and metrics (Disaster Score). Makes broad and generic statements instead of specific recommendations."
    },
    "PR Manager 🤝": {
        "text": "We're thrilled to share our feedback! Customers love our top-notch bread, fresh sushi, and outstanding coffee. As an 'opportunity to grow', we noticed a few guests experienced long wait times and felt our menu was a bit small. We are committed to improving!\n\n**Customer Happiness Score: 8/10**",
        "accuracy": "4/5",
        "actionability": "4/5",
        "feedback": "Mostly accurate, but slightly intensifies the tone. Actionable insights are clear."
    },
    "Baseline Consultant 💼": {
        "text": "**Good:** Top-notch bread, fresh sushi, delightful service, incredible taglierini with truffles.\n\n**Bad:** Mediocre portions, reheated food, wasted steaks, dreadful service.\n\n**Recommendation:** The restaurant excels in providing fresh food, but needs to strictly address the kitchen's reliance on reheated meals and improve service speed.",
        "accuracy": "4/5",
        "actionability": "3/5",
        "feedback": "Mostly accurate, but slightly intensifies tone. Stops short of concrete, step-by-step business recommendations."
    },
    "JSON Strict 💻": {
        "text": "{\n  'top_complaint': ['mediocre portions', 'wasted steaks', 'expensive', 'reheated food'],\n  'top_praise': ['spicy tuna roll', 'best lasagna', 'fresh sushi', 'melts in your mouth'],\n  'action_item': ['Improve food consistency and freshness to address complaints about reheated food.']\n}",
        "accuracy": "4/5",
        "actionability": "4/5",
        "feedback": "Identifies specific operational issues and links them to clear business recommendations. Highly structured."
    },
    "Gen Z TikToker 📱": {
        "text": "Foodie alert! 🍴👀 Some restaurants serve up top-notch eats 🍔🍣, while others fall flat 🤦‍♂️🍕. From fresh sushi 🍣 to mediocre portions 🤔, the verdict is in: quality matters most! 👍 #foodreview #restaurantlife",
        "accuracy": "2/5",
        "actionability": "1/5",
        "feedback": "Invents several terms, emojis, and hashtags not present in the data. Zero actionable insights."
    },
    "Chief Operations Officer 🏢": {
        "text": "**Quality Control Failures:** Inconsistent food preparation (reheated dishes) and unacceptable wait times.\n\n**SOP Updates:** Implement a 'cook-to-order' policy. Adjust kitchen staffing during peak periods.\n\n**Operational Readiness Score: 72/100**",
        "accuracy": "2/5",
        "actionability": "3/5",
        "feedback": "Invents specific corporate entities/metrics (Quality Control Failures, SOP Updates) not mentioned in original reviews."
    },
    "Health & Safety Inspector 🔬": {
        "text": "**Violation Report**\nOne reviewer mentions that the food was 'obviously made before hand and then reheated', indicating a potential food safety risk of undercooked or improperly stored food. Immediate action required to ensure safe internal temperatures.\n\n**Health Risk Score: 6/10**",
        "accuracy": "1/5",
        "actionability": "1/5",
        "feedback": "FATAL HALLUCINATION. Invents a food safety risk. The data mentions reheated food, but does not indicate any safety/health risks."
    },
    "Instagram Influencer 📸": {
        "text": "OH MY GOSH, GUYS!!! 🤩 I just discovered the most AMAZING restaurants! First up, Sushi Rose 🍣! And if you're craving Italian, MJ Grill 🍴 is the way to go! Don't forget Cabana 🤯!\n\n**Vibe Check Score: 10/10**",
        "accuracy": "1/5",
        "actionability": "1/5",
        "feedback": "HALLUCINATION - the summary invents specific restaurant names (Sushi Rose, MJ Grill, Cabana) not mentioned in the original data."
    },
    "Competitor Owner 😈": {
        "text": "**Staff Memo:** Our competitor has good sushi and bread. However, they suffer from dreadful service, 45-minute wait times, and watered-down drinks. We can exploit these weaknesses by emphasizing our prompt service and made-to-order dishes!\n\n**Competitor Vulnerability Score: 6/10**",
        "accuracy": "2/5",
        "actionability": "3/5",
        "feedback": "Invents specific entities and metrics (competitor's strengths) not present in the data."
    },
    "Action-Item JSON ⚙️": {
        "text": "[\n  { 'dish': 'Sushi', 'type': 'praise', 'action': 'Maintain quality' },\n  { 'dish': 'Dessert Pizza', 'type': 'issue', 'action': 'Improve prep time' },\n  { 'dish': 'Steaks', 'type': 'issue', 'action': 'Improve cooking quality' }\n]",
        "accuracy": "4/5",
        "actionability": "3/5",
        "feedback": "Mostly accurate, capturing praises and issues. Lacks specificity in suggested actions (e.g., 'Maintain quality' is too broad)."
    },
    "Financial Auditor 📉": {
        "text": "**Cost-Impact Summary:** The kitchen is losing money due to incorrect orders (wasted ingredients), slow service (lost sales, labor costs), and food waste from reheated dishes being sent back.\n\n**Financial Efficiency Score: 6/10**",
        "accuracy": "4/5",
        "actionability": "3/5",
        "feedback": "Mostly accurate, but intensifies tone by stating 'Operational Waste'. Actionable insights are moderately specific."
    },
    "Haiku Poet 🌸": {
        "text": "Fresh and clean delight\nSushi rolls a pleasure here\nQuality in bite\n\nAttentive and kind\nStaff a pleasure to meet here\nHospitality",
        "accuracy": "5/5",
        "actionability": "3/5",
        "feedback": "Fully accurate, capturing the essence without inventing claims. Moderate actionability due to poetic format."
    },
    "Customer Success Mgr 📧": {
        "text": "Subject: Apology for Your Experience\n\nDear Customer, I am sincerely sorry about the reheated dishes, mediocre portions, and unappetizing presentation. We would like to offer you a complimentary meal on your next visit...\n\nBest, Restaurant Owner",
        "accuracy": "1/5",
        "actionability": "1/5",
        "feedback": "FATAL HALLUCINATION. Invents specific complaints (unappetizing presentation) and offers generic solutions."
    },
    "Menu Engineer 📜": {
        "text": "**Chef's Specials:**\n* Spicy Tuna Roll\n* Asian Salad\n* Lasagna\n\n**Dishes to Remove:**\n* NICOISE Salad (barely eatable)\n* Dessert Pizza (takes 45 mins)\n\n**Recommendation:** Highlight the specials and remove the problematic dishes to improve dining experience.",
        "accuracy": "4/5",
        "actionability": "4/5",
        "feedback": "Mostly accurate, but implies these are the only notable dishes. Clear and actionable recommendations."
    },
    "AI Evaluator (Meta) 🤖": {
        "text": "STATUS: PASS\n\nThe main reason is that the overall sentiment of the food is more positive than negative, with many customers praising the freshness, quality, and taste of the dishes.",
        "accuracy": "4/5",
        "actionability": "3/5",
        "feedback": "Accurate assessment of overall sentiment, but lacks specific actionable insights or operational recommendations."
    }
}

# Initialize votes
votes = get_vote_tally()

# Initialize user state (to prevent voting multiple times from the same browser tab)
if "has_voted" not in st.session_state:
    st.session_state.has_voted = False

# --- UI (USER INTERFACE) ---
st.title("🤖 AI Persona Evaluator")
st.markdown("### Restaurant: **Sushi Rose** 🍣")
st.write("We asked an AI to analyze reviews using different 'personas'. Read them below, check the AI Judge's score, and vote for your favorite!")
st.divider()

# 1. Persona Selection
selected_persona = st.selectbox("👇 Choose a Persona to read:", list(PERSONAS_DATA.keys()))
data = PERSONAS_DATA[selected_persona]

# 2. Display the Response
st.markdown(f"**{selected_persona} says:**")
st.markdown(f"<div class='persona-box'>{data['text']}</div>", unsafe_allow_html=True)

# 3. What the LLM Judge says (Hidden by default)
with st.expander("⚖️ See LLM Judge Evaluation"):
    col1, col2 = st.columns(2)
    col1.metric("Accuracy", data["accuracy"])
    col2.metric("Actionability", data["actionability"])
    st.info(f"**Judge Feedback:** {data['feedback']}")

st.divider()

# 4. Voting Section
if not st.session_state.has_voted:
    st.subheader("Did you like this output?")
    if st.button(f"🗳️ Vote for {selected_persona}", type="primary"):
        votes[selected_persona] += 1
        st.session_state.has_voted = True
        st.rerun() # Refresh the page to update the UI and show statistics
else:
    st.success("🎉 Thanks for voting! Here are the live results:")
    
    # Display Vote Chart
    df_votes = pd.DataFrame(list(votes.items()), columns=["Persona", "Votes"])
    
    # Sort descending to make the chart look organized
    df_votes = df_votes.sort_values(by="Votes", ascending=True) 
    
    fig = px.bar(df_votes, x="Votes", y="Persona", orientation='h', 
                 title="Live Leaderboard 🏆", color="Votes", color_continuous_scale="Viridis")
    
    fig.update_layout(xaxis=dict(dtick=1)) # Force integer ticks on the X axis (1, 2, 3...)    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("Refresh the page to see updated global votes.")
