
import streamlit as st
import time

st.set_page_config(page_title="SmartQuizzer", layout="wide")

# ================= QUESTIONS =================
questions = {
    "Easy": [
        {"q": "🤖 What is Machine Learning?", "opts": ["Subset of AI", "Database", "Hardware", "Web Tool"],
         "ans": "Subset of AI", "exp": "Machine Learning is a subset of Artificial Intelligence."},
        {"q": "📊 ML works mainly on?", "opts": ["Data", "Hardware", "Cables", "Design"],
         "ans": "Data", "exp": "ML learns patterns from data."},
        {"q": "🐍 Which language is popular for ML?", "opts": ["Python", "HTML", "CSS", "JavaScript"],
         "ans": "Python", "exp": "Python is widely used for ML."},
        {"q": "🧠 ML is part of which field?", "opts": ["AI", "DBMS", "OS", "Networking"],
         "ans": "AI", "exp": "ML comes under Artificial Intelligence."},
        {"q": "📚 Which is an ML library?", "opts": ["Scikit-learn", "Bootstrap", "React", "Angular"],
         "ans": "Scikit-learn", "exp": "Scikit-learn is an ML library."}
    ],
    "Medium": [
        {"q": "🌳 Which algorithm is used for classification?", "opts": ["Decision Tree", "K-Means", "Apriori", "PCA"],
         "ans": "Decision Tree", "exp": "Decision Trees are used for classification."},
        {"q": "🏷️ What is supervised learning?", "opts": ["Labeled data", "No data", "Random learning", "Unlabeled data"],
         "ans": "Labeled data", "exp": "Uses labeled datasets."},
        {"q": "🔍 Which is an unsupervised algorithm?", "opts": ["K-Means", "SVM", "Naive Bayes", "Decision Tree"],
         "ans": "K-Means", "exp": "K-Means is unsupervised."},
        {"q": "✅ Accuracy is used for?", "opts": ["Classification", "Clustering", "Regression", "Cleaning"],
         "ans": "Classification", "exp": "Accuracy evaluates classification models."},
        {"q": "🧪 Train-test split is used for?", "opts": ["Model evaluation", "UI design", "Deployment", "Cleaning"],
         "ans": "Model evaluation", "exp": "Used to evaluate ML models."}
    ],
    "Difficult": [
        {"q": "⚠️ What is overfitting?", "opts": ["Model performs well on training but poorly on new data",
                                                "Model trains very fast", "Model has less data",
                                                "Model always performs poorly"],
         "ans": "Model performs well on training but poorly on new data",
         "exp": "Overfitting memorizes training data."},
        {"q": "🛠️ Which technique reduces overfitting?", "opts": ["Regularization", "More epochs",
                                                                  "High learning rate", "No validation"],
         "ans": "Regularization", "exp": "Controls model complexity."},
        {"q": "⚖️ Bias-Variance tradeoff is related to?", "opts": ["Model performance", "Hardware",
                                                                   "Database", "Frontend"],
         "ans": "Model performance", "exp": "Affects accuracy."},
        {"q": "🌲 Which is an ensemble method?", "opts": ["Random Forest", "KNN",
                                                           "Linear Regression", "K-Means"],
         "ans": "Random Forest", "exp": "Uses multiple models."},
        {"q": "🔁 Cross-validation is used for?", "opts": ["Reliable evaluation", "Deployment",
                                                            "Cleaning", "Visualization"],
         "ans": "Reliable evaluation", "exp": "Improves evaluation reliability."}
    ]
}

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "start"
if "level" not in st.session_state:
    st.session_state.level = None
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {"Easy": [], "Medium": [], "Difficult": []}
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ================= START PAGE =================
st.title("🧠 SmartQuizzer")

if st.session_state.page == "start":
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")

    if st.button("Start Quiz"):
        if name and email:
            st.session_state.page = "level_select"
            st.rerun()
        else:
            st.warning("Enter Name and Email")

# ================= LEVEL SELECTION =================
elif st.session_state.page == "level_select":
    st.subheader("📦 Select Difficulty")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Easy")
        if st.button("Start Easy"):
            st.session_state.level = "Easy"
            st.session_state.q_index = 0
            st.session_state.start_time = time.time()
            st.session_state.page = "quiz"
            st.rerun()

    with col2:
        st.info("Medium")
        if st.button("Start Medium"):
            st.session_state.level = "Medium"
            st.session_state.q_index = 0
            st.session_state.start_time = time.time()
            st.session_state.page = "quiz"
            st.rerun()

    with col3:
        st.info("Difficult")
        if st.button("Start Difficult"):
            st.session_state.level = "Difficult"
            st.session_state.q_index = 0
            st.session_state.start_time = time.time()
            st.session_state.page = "quiz"
            st.rerun()

# ================= QUIZ PAGE =================
elif st.session_state.page == "quiz":
    level = st.session_state.level
    qlist = questions[level]

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 20 - elapsed)
    st.info(f"⏱ {level} Time Remaining: {remaining} seconds")

    q = qlist[st.session_state.q_index]
    st.subheader(f"{level} Question {st.session_state.q_index + 1}")
    st.write(q["q"])

    choice = st.radio("Choose your answer", q["opts"],
                      key=f"{level}_{st.session_state.q_index}")

    if st.button("Submit") or remaining == 0:
        st.session_state.answers[level].append(choice if remaining > 0 else None)
        st.session_state.q_index += 1
        st.session_state.start_time = time.time()

        if st.session_state.q_index == 5:
            st.session_state.page = "level_select"

        st.rerun()

# ================= RESULT PAGE =================
if all(len(st.session_state.answers[lvl]) == 5 for lvl in ["Easy", "Medium", "Difficult"]):
    st.header("📊 Score Board")

    total = 0
    for lvl in ["Easy", "Medium", "Difficult"]:
        st.subheader(lvl)
        correct = 0
        for i, q in enumerate(questions[lvl]):
            if st.session_state.answers[lvl][i] == q["ans"]:
                correct += 1
            else:
                st.write(f"❌ {q['q']}")
                st.write(f"✔ Correct: {q['ans']}")
                st.write(f"📘 Explanation: {q['exp']}")
        score = correct * (50 // 15)
        st.write(f"**{lvl} Score: {score}**")
        total += score

    st.success(f"🏆 Total Score: {total} / 50")
    st.markdown("## 🎉 Congratulations!")
    st.balloons()