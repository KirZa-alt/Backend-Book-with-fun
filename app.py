import streamlit as st
import random
import json
import os

# --- Save Progress ---
def save_progress():
    progress = {
        "xp": st.session_state.get("xp", 0),
        "game_xp": st.session_state.get("game_xp", 0),
        "completed_chapters": st.session_state.get("completed_chapters", [])
    }
    with open("progress.json", "w") as f:
        json.dump(progress, f)

# --- Load Progress ---
def load_progress():
    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            data = json.load(f)
            st.session_state.xp = data.get("xp", 0)
            st.session_state.game_xp = data.get("game_xp", 0)
            st.session_state.completed_chapters = data.get("completed_chapters", [])
    else:
        st.session_state.xp = 0
        st.session_state.game_xp = 0
        st.session_state.completed_chapters = []

# --- Initialize on app start ---
if "xp" not in st.session_state:
    load_progress()


# Initialize state
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "completed_chapters" not in st.session_state:
    st.session_state.completed_chapters = set()


# Sidebar Theme Toggle (only one place)
with st.sidebar:
    theme = st.radio(
        "Choose Theme:", 
        ["🌞 Light", "🌙 Dark"], 
        key="theme_toggle_sidebar"
    )

# Apply selected theme
if theme == "🌙 Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: #ffffff;
        }
        .stButton button {
            background-color: #333333;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Save theme
def save_theme(theme_choice):
    st.session_state.theme = theme_choice
    save_progress()

# When user changes theme
theme = st.radio("Choose Theme:", ["🌞 Light", "🌙 Dark"], key="theme_toggle")
save_theme(theme)


# --- 📊 Dashboard Page ---
def progress_dashboard():
    st.title("📊 Progress Dashboard")

    # XP Section
    st.subheader("⭐ Total XP Earned")
    st.metric("XP", f"{st.session_state.xp}")

    # Chapters Progress
    total_chapters = 20   # you have 20 chapters
    completed = len(st.session_state.completed_chapters)
    progress = completed / total_chapters

    st.subheader("📘 Chapters Completed")
    st.progress(progress)
    st.write(f"{completed} / {total_chapters} chapters completed")

    # 🏆 Badges & Milestones
    st.subheader("🏆 Badges Earned")
    badges = []

    if completed >= 1:
        badges.append("🎯 Beginner Explorer")
    if completed >= 6:
        badges.append("🔐 Authentication Master")
    if completed >= 12:
        badges.append("🧪 Testing Pro")
    if completed == total_chapters:
        badges.append("🚀 Full Stack Champion")

    if badges:
        for b in badges:
            st.success(b)
    else:
        st.info("No badges yet. Keep learning! 💪")

# Call this when user clicks "Dashboard"
if st.sidebar.button("📊 Go to Dashboard"):
    progress_dashboard()
    save_progress()

# --- Initialize session state for gamification ---
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = 1


# Chapter details (auto dictionary)
chapters_info = {
    1: {"title": "Intro to Backend", "subtitle": "Frontend vs Backend – What’s the difference?", "emoji": "🌐"},
    2: {"title": "Node.js Basics", "subtitle": "JavaScript outside the browser!", "emoji": "⚡"},
    3: {"title": "Express.js", "subtitle": "Framework for building backend apps", "emoji": "🚀"},
    4: {"title": "Databases & MongoDB", "subtitle": "Storing and retrieving data", "emoji": "🗄️"},
    5: {"title": "REST APIs", "subtitle": "Connecting frontend & backend seamlessly", "emoji": "🔗"},
    6: {"title": "Authentication & Security", "subtitle": "Keeping users safe", "emoji": "🔒"},
    7: {"title": "REST APIs & CRUD (Deep)", "subtitle": "Create, Read, Update, Delete in depth", "emoji": "🛠️"},
    8: {"title": "Deployment & Hosting", "subtitle": "How to put your app online", "emoji": "🌍"},
    9: {"title": "Advanced Backend Concepts", "subtitle": "Scaling and optimization", "emoji": "⚙️"},
    10: {"title": "Microservices", "subtitle": "Breaking apps into smaller services", "emoji": "🔄"},
    11: {"title": "Real-Time Backend & WebSockets", "subtitle": "Live chat & real-time apps", "emoji": "💬"},
    12: {"title": "Testing & Debugging", "subtitle": "Making sure your backend works perfectly", "emoji": "🐞"},
    13: {"title": "CI/CD & Automated Deployment", "subtitle": "Ship faster with automation", "emoji": "🤖"},
    14: {"title": "Monitoring & Logging", "subtitle": "Track performance & errors", "emoji": "📊"},
    15: {"title": "Scaling & Load Balancing", "subtitle": "Handling millions of users", "emoji": "📈"},
    16: {"title": "Containerization with Docker", "subtitle": "Portable backend apps", "emoji": "🐳"},
    17: {"title": "Kubernetes & Orchestration", "subtitle": "Managing many containers", "emoji": "☸️"},
    18: {"title": "Cloud Deployment (AWS/GCP/Azure)", "subtitle": "Hosting in the cloud", "emoji": "☁️"},
    19: {"title": "CI/CD Pipelines", "subtitle": "Automating workflows", "emoji": "🛠️"},
    20: {"title": "WebSockets", "subtitle": "Real-time connections", "emoji": "🔌"},
    21: {"title": "Coding Games", "subtitle": "Learn through fun backend challenges", "emoji": "🎮"}
}

# Function to display divider
def chapter_divider(chapter_num):
    info = chapters_info.get(chapter_num, {})
    st.markdown(f"""
        <div style="
            background: rgba(0, 0, 128, 0.5);
            padding: 90px;
            border-radius: 25px;
            text-align: center;
            margin-bottom: 40px;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.6);
        ">
            <h1 style="color:#FFD700; font-size:70px; font-family:Georgia, serif;">
                {info.get('emoji','📘')} Chapter {chapter_num}: {info.get('title','')}
            </h1>
            <h3 style="color:white; font-size:28px; font-family:Trebuchet MS, sans-serif; opacity:0.95;">
                {info.get('subtitle','')}
            </h3>
        </div>
    """, unsafe_allow_html=True)

# Set background image with CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1507842217343-583bb7270b66");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.block-container {
    background: rgba(0,0,0,0.7);
    padding: 80px;
    border-radius: 15px;
    max-width: 1000px;            /* ✅ Limit width so it looks like a "page" */
    box-shadow: 0px 0px 25px rgba(0,0,0,0.8); /* ✅ Nice shadow */
}
h1, h2, h3, h4, h5, h6 {
    color: Yellow !important;       /* ✅ All headings red */
    font-size: 36px !important;  /* ✅ Bigger headings */
    font-weight: bold !important;
}

/* Paragraph text */
p, li, span, label {
    font-size: 22px !important;
}
</style>
"""


st.markdown(page_bg_img, unsafe_allow_html=True)


if "score" not in st.session_state:
    st.session_state.score = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

st.sidebar.title("📚 Chapters")
chapter = st.sidebar.radio(
    "Go to", 
    [
        "Home", 
        
        "Chapter 1: Intro to Backend", "Chapter 1 Quiz", "Chapter 1 Tasks",
        
        "Chapter 2: Node.js Basics", "Chapter 2 Quiz", "Chapter 2 Tasks",
        
        "Chapter 3: Express.js", "Chapter 3 Quiz", "Chapter 3 Tasks",

        "Chapter 4: Databases & MongoDB", "Chapter 4 Quiz", "Chapter 4 Tasks",

        "Chapter 5: REST APIs", "Chapter 5 Quiz", "Chapter 5 Tasks",

        "Chapter 6: Authentication & Security", "Chapter 6 Quiz", "Chapter 6 Tasks",

        "Chapter 7: REST APIs & CRUD (Deep)", "Chapter 7 Quiz", "Chapter 7 Tasks",

        "Final Project: Chapters 1–7",

        "Chapter 8: Deployment & Hosting", "Chapter 8 Quiz","Chapter 8 Tasks",

        "Chapter 9: Advanced Backend Concepts (Deep)", "Chapter 9 Quiz","Chapter 9 Tasks",

        "Chapter 10: Microservices", "Chapter 10 Quiz", "Chapter 10 Tasks",

        "Chapter 11: Real-Time Backend & WebSockets", "Chapter 11 Quiz", "Chapter 11 Tasks",

        "Chapter 12: Testing & Debugging", "Chapter 12 Quiz", "Chapter 12 Tasks",

        "Chapter 13: CI/CD & Automated Deployment", "Chapter 13 Quiz","Chapter 13 Tasks",

        "Chapter 14: Monitoring & Logging", "Chapter 14 Quiz","Chapter 14 Tasks",

        "Chapter 15: Scaling & Load Balancing", "Chapter 15 Quiz","Chapter 15 Tasks",

        "Chapter 16: Containerization with Docker", "Chapter 16 Quiz","Chapter 16 Tasks",

        "Chapter 17: Kubernetes & Orchestration", "Chapter 17 Quiz","Chapter 17 Tasks",

        "Chapter 18: Cloud Deployment (AWS/GCP/Azure)", "Chapter 18 Quiz","Chapter 18 Tasks",

        "Chapter 19: CI/CD Pipelines", "Chapter 19 Quiz","Chapter 19 Tasks",

        "Chapter 20: WebSockets", "Chapter 20 Quiz","Chapter 20 Tasks",

        "Coding Games"
    ]
    
)
# 🎮 Gamification Progress
st.sidebar.markdown("## 🎯 Progress Tracker")
level = st.session_state.xp // 50 + 1
progress = (st.session_state.xp % 50) / 50

st.sidebar.progress(progress)
st.sidebar.write(f"🏆 Level {level}")
st.sidebar.write(f"⭐ XP: {st.session_state.xp}")

# Bonus roll button
if st.sidebar.button("🎲 Roll Bonus"):
    bonus = random.choice([0, 5, 10, 20])
    st.session_state.xp += bonus
    st.sidebar.success(f"🎉 You got +{bonus} XP!")




if st.session_state.total_questions > 0:
    st.sidebar.markdown(f"### 📊 Progress")
    st.sidebar.progress(st.session_state.score / st.session_state.total_questions)
    st.sidebar.write(f"Score: {st.session_state.score}/{st.session_state.total_questions}")


# Home Page
if chapter == "Home":
    st.title("📘 Backend Learning Book for My Love ❤️")
    st.write("**Welcome! This is your interactive book to learn Backend Development step by step.**")
    st.write("**👉 Use the sidebar to start your journey.**")
    
elif chapter == "Chapter 1: Intro to Backend":
    st.header("🌐 Chapter 1: Intro to Backend")
    chapter_divider(1)

    st.write("""
    When you open a website or app, what you see and interact with is the **frontend**.  
    But what happens behind the scenes — the part you don’t see — is the **backend**.

    🔹 **What is Backend?**
    - Backend is the "brain" of an application.  
    - It handles requests, applies logic, connects with databases, and returns responses.  
    - Without backend, the frontend would just be static pages.  

    🔹 **Example**
    Imagine logging into Facebook:  
    - Frontend shows the login form.  
    - Backend checks your username & password in the database.  
    - If correct → backend sends "success", frontend shows your profile.  
    - If wrong → backend sends "error", frontend shows a warning.  

    🔹 **Main Roles of Backend**
    1. **Logic** – Decides what happens (e.g., if a user clicks “Buy”, backend processes payment).  
    2. **Database** – Stores and retrieves information (users, posts, messages, etc.).  
    3. **Authentication** – Verifies identity (logins, permissions).  
    4. **APIs** – Provides communication between frontend and backend.  

    👉 In short: **Frontend is what users see, Backend is how everything works.**
    """)

    st.info("📖 After reading, go to **'Chapter 1 Quiz'** from the sidebar to test yourself!")
    st.markdown("📺 **Learn More (Video in Hindi):** [Chai aur JavaScript - Backend Intro](https://www.youtube.com/playlist?list=PLu71SKxNbfoBGh_8p_NS-ZAh6v7HhYqHW)")
    
elif chapter == "Chapter 1 Quiz":
    st.header("🧩 Chapter 1 Quiz: Intro to Backend")
    st.write("Test your understanding of Chapter 1 before moving on 🚀")

    score = 0

    # Q1
    q1 = st.radio(
        "1️⃣ Which of these is NOT part of the backend?",
        ["Database", "Server", "HTML", "API"],
        index=None,
        key="c1_q1"
    )
    if q1:
        if q1 == "HTML":
            st.success("✅ Correct! HTML is frontend.")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong, try again!")

    st.markdown("---")

    # Q2
    q2 = st.radio(
        "2️⃣ What does the backend mainly handle?",
        ["Design & Layout", "Data & Logic", "Animations", "Colors"],
        index=None,
        key="c1_q2"
    )
    if q2:
        if q2 == "Data & Logic":
            st.success("✅ Correct! Backend handles logic and data.")
            score += 1
            save_progress()
        else:
            st.error("❌ Nope, that’s frontend stuff!")

    st.markdown("---")

    # Q3
    q3 = st.radio(
        "3️⃣ When you log into Facebook, what part checks your password?",
        ["Frontend", "Backend", "Browser", "CSS"],
        index=None,
        key="c1_q3"
    )
    if q3:
        if q3 == "Backend":
            st.success("🎉 Perfect! Backend checks credentials.")
            score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Not correct.")

    st.markdown("---")

    # ✅ Show results once all answered
    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {score}/3")
        if score >= 2:
            if "quiz1_done" not in st.session_state:  # give XP only once
                st.session_state.xp += 10
                st.session_state.quiz1_done = True

                # 🔑 Mark Chapter 1 as completed
                st.session_state.completed_chapters.add(1)
            st.success("🏆 Great job! You earned +10 XP.")
            save_progress()

        else:
            st.warning("💡 Keep practicing, you need at least 2 correct to earn XP.")

    
elif chapter == "Chapter 2: Node.js Basics":
    st.header("⚡ Chapter 2: Node.js Basics")
    chapter_divider(2)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    **Node.js** is a runtime that allows you to run **JavaScript outside the browser**.  
    It is often used to build **backend servers**.

    🔹 **Why Node.js?**
    - Uses JavaScript (which you already know from frontend).  
    - Non-blocking, event-driven → handles many requests efficiently.  
    - Huge ecosystem (NPM packages).  

    🔹 **Example: A Simple Server**
    In Node.js, you can create a server in just a few lines:

    ```javascript
    const http = require('http');
    const server = http.createServer((req, res) => {
      res.write("Hello from Backend!");
      res.end();
    });
    server.listen(3000);
    ```

    - `http` → built-in module for creating servers.  
    - `createServer` → defines what happens when a request comes.  
    - `listen(3000)` → runs server on port 3000.  

    👉 This is the starting point of backend with Node.js.
    """)

    st.info("📖 After reading, go to **'Chapter 2 Quiz'** from the sidebar to test yourself!")
    st.markdown("📺 **Learn More (Video in Hindi):** [CodeWithHarry - Node.js Playlist](https://www.youtube.com/playlist?list=PLu0W_9lII9ajyk081To1Cbt2eI5913SsL)")
elif chapter == "Chapter 2 Quiz":
    st.header("🧩 Chapter 2 Quiz: Node.js Basics")
    st.write("Test your knowledge of Node.js before moving forward 🚀")

    score = 0  # local score counter

    # Q1
    q1 = st.radio(
        "1️⃣ What language does Node.js use?",
        ["Python", "Java", "JavaScript", "C++"],
        index=None,
        key="c2_q1"
    )
    if q1:
        if q1 == "JavaScript":
            st.success("✅ Correct! Node.js runs JavaScript.")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong, try again!")

    st.markdown("---")

    # Q2
    q2 = st.radio(
        "2️⃣ Which command starts a Node.js server on port 3000?",
        [
            "server.start(3000)",
            "server.listen(3000)",
            "run server 3000",
            "server.open(3000)"
        ],
        index=None,
        key="c2_q2"
    )
    if q2:
        if q2 == "server.listen(3000)":
            st.success("✅ Correct! `listen` is used to start the server.")
            score += 1
            save_progress()
        else:
            st.error("❌ Nope, check the code example again!")

    st.markdown("---")

    # Q3
    q3 = st.radio(
        "3️⃣ What is Node.js mainly used for?",
        ["Frontend design", "Backend servers", "Making CSS prettier", "Image editing"],
        index=None,
        key="c2_q3"
    )
    if q3:
        if q3 == "Backend servers":
            st.success("🎉 Correct! Node.js is great for backend.")
            score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Wrong answer.")

    st.markdown("---")

    # Final Score + XP
    if q1 and q2 and q3:
        st.subheader(f"📊 Your Score: {score} / 3")
        if score == 3:
            st.success("🌟 Excellent! You mastered Node.js basics.")
        elif score >= 2:
            st.info("👍 Good effort! Review once more for perfection.")
        else:
            st.warning("💡 Keep practicing. Don’t worry, you’ll get better.")

        # ✅ Award XP only once
        if "quiz2_done" not in st.session_state:
            st.session_state.xp += 10
            st.session_state.quiz2_done = True
            st.success("🏆 You earned +10 XP!")
            save_progress()

            # 🔑 Mark Chapter 1 as completed
            st.session_state.completed_chapters.add(2)
            save_progress()

elif chapter == "Chapter 3: Express.js":
    st.header("🚀 Chapter 3: Express.js Framework")
    chapter_divider(3)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    **Express.js** is a lightweight framework for **Node.js** that makes building backend servers much easier.  

    🔹 **Why Express?**
    - Node.js is powerful but writing servers with pure `http` module can get long and messy.  
    - Express simplifies things by giving easy methods for routes, middleware, and APIs.  

    🔹 **Hello World in Express**
    ```javascript
    const express = require('express');
    const app = express();

    app.get('/', (req, res) => {
      res.send('Hello from Express!');
    });

    app.listen(3000, () => {
      console.log("Server running on port 3000");
    });
    ```
    - `express()` → creates an Express app  
    - `app.get('/', ...)` → defines what happens at the homepage  
    - `app.listen(3000)` → starts the server at **http://localhost:3000**

    🔹 **Multiple Routes**
    ```javascript
    app.get('/about', (req, res) => {
      res.send('This is the About Page');
    });

    app.get('/contact', (req, res) => {
      res.send('Contact us at: hello@example.com');
    });
    ```
    - `/about` → About page  
    - `/contact` → Contact page  

    👉 Express.js is the foundation for many big apps and APIs.
    """)

    st.info("📖 After reading, go to **'Chapter 3 Quiz'** from the sidebar to test yourself!")
    st.markdown("📺 **Learn More (Video in Hindi):** [Chai aur Code - Express.js Tutorial](https://www.youtube.com/playlist?list=PLu71SKxNbfoC0jOwtjJCBn2VQOzjMUkfZ)")

elif chapter == "Chapter 3 Quiz":
    st.header("🧩 Chapter 3 Quiz: Express.js Basics")
    st.write("Let’s see how well you understood Express.js 🚀")

    score = 0

    # Q1
    q1 = st.radio(
        "1️⃣ What is Express.js mainly used for?",
        ["Designing Frontend", "Building Backend Servers", "Styling with CSS", "Creating Databases"],
        index=None,
        key="c3_q1"
    )
    if q1:
        if q1 == "Building Backend Servers":
            st.success("✅ Correct! Express is a backend framework.")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong answer.")

    st.markdown("---")

    # Q2
    q2 = st.radio(
        "2️⃣ In Express.js, which method is used to define a GET route?",
        ["app.route()", "app.fetch()", "app.get()", "app.start()"],
        index=None,
        key="c3_q2"
    )
    if q2:
        if q2 == "app.get()":
            st.success("✅ Correct! `app.get()` defines GET routes.")
            score += 1
            save_progress()
        else:
            st.error("❌ Nope, that’s not right.")

    st.markdown("---")

    # Q3
    q3 = st.radio(
        "3️⃣ Which line starts the Express server on port 3000?",
        [
            "app.run(3000)",
            "app.open(3000)",
            "app.listen(3000)",
            "server.start(3000)"
        ],
        index=None,
        key="c3_q3"
    )
    if q3:
        if q3 == "app.listen(3000)":
            st.success("🎉 Correct! That’s how you start the server.")
            score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Wrong, check the example code again!")

    st.markdown("---")

    # ✅ Show results
    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {score}/3")
        if score >= 2:  # passing condition
            if "quiz3_done" not in st.session_state:  # prevent multiple XP gains
                st.session_state.xp += 10
                st.session_state.quiz3_done = True

                # 🔑 Mark Chapter 1 as completed
                st.session_state.completed_chapters.add(3)
            st.success("🏆 Well done! You earned +10 XP.")
            save_progress()
        else:
            st.warning("⚠️ You scored less than 2. Try again to earn XP.")

    # Final Score
    if q1 and q2 and q3:
        st.subheader(f"📊 Your Score: {st.session_state.score} / {st.session_state.total_questions}")
        if st.session_state.score == st.session_state.total_questions:
            st.success("🌟 Excellent! You’re ready for the next chapter.")
        elif st.session_state.score >= 2:
            st.info("👍 Good job! Review once more for full confidence.")
        else:
            st.warning("💡 Keep practicing Express basics.")
        st.session_state.xp += 10
    st.success("✅ You earned 10 XP!")    

elif chapter == "Chapter 1 Tasks":
    st.header("📝 Chapter 1 Tasks: Intro to Backend")
    st.write("""
    These tasks will help you practice the fundamentals of backend concepts.
    """)

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Write a simple Python program that prints:
       - `"This is Frontend"`  
       - `"This is Backend"`  
       (Helps you understand separation of concerns.)  

    2. Create a Python dictionary called `server_response` that looks like JSON.

    3. Simulate a **client request**:
       - Input your name.  
       - Print a message: `"Hello <name>, server received your request."`
    """)


elif chapter == "Chapter 2 Tasks":
    st.header("📝 Chapter 2 Tasks: Node.js Basics")
    st.write("""
    Practice Node.js by building small scripts.
    """)

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Write a Node.js script that prints `"Hello Backend World!"`.  

    2. Create a program that prints current **date & time**.  

    3. Build a simple calculator in Node.js that:
       - Takes two numbers as input.  
       - Prints their sum.  

    4. Create a Node.js program that reads `data.txt` file and prints its content.
    """)


elif chapter == "Chapter 3 Tasks":
    st.header("📝 Chapter 3 Tasks: Express.js Framework")
    st.write("""
    Practice Express.js by building small servers.
    """)

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Install Express.js and create a simple server.

    2. Add two new routes:
       - `/about` → returns `"This is About Page"`  
       - `/contact` → returns `"This is Contact Page"`

    3. Create middleware that logs every request method + URL.

    4. Build a small **Quotes API**:
       - `/quotes` → returns an array of 5 quotes in JSON.
    """)

elif chapter == "Chapter 4: Databases & MongoDB":
    st.header("💾 Chapter 4: Databases & MongoDB")
    chapter_divider(4)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    Databases are used to **store and organize data** so applications can use it later.  
    Without databases, everything would be lost when the app restarts.

    ### 🔹 Why Databases?
    - Store user accounts, orders, products, messages.
    - Keep data safe and persistent.
    - Allow multiple users to access the same data.

    ### 🔹 Types of Databases
    1. **SQL (Relational Databases)** → store data in **tables** (MySQL, PostgreSQL).
    2. **NoSQL (Document Databases)** → store data as **JSON-like documents** (MongoDB).

    Example MongoDB Document:
    ```json
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com",
      "isAdmin": true
    }
    ```

    ### 🔹 MongoDB Basics
    - **Database** → Collection of data  
    - **Collection** → Group of documents  
    - **Document** → One JSON object (like a row in SQL)  

    ### 🔹 CRUD Operations
    - **Create** → Insert new data  
    - **Read** → Get data from DB  
    - **Update** → Change data  
    - **Delete** → Remove data  

    ### 🔹 Example: Node.js + MongoDB
    ```javascript
    const mongoose = require("mongoose");

    // connect to DB
    mongoose.connect("mongodb://localhost:27017/myapp");

    // define schema
    const UserSchema = new mongoose.Schema({
      name: String,
      email: String,
      age: Number
    });

    const User = mongoose.model("User", UserSchema);

    // create and save
    const newUser = new User({ name: "Alice", email: "alice@example.com", age: 25 });
    newUser.save().then(() => console.log("User saved!"));
    ```
    """)

    st.markdown("📺 **Learn More (Video in Hindi):** [CodeWithHarry - MongoDB Tutorial](https://www.youtube.com/playlist?list=PLu0W_9lII9ah7DDtYtflgwMwpT3xmjXY9)")

elif chapter == "Chapter 4 Quiz":
    st.header("🧩 Chapter 4 Quiz: Databases & MongoDB")

    score = 0

    q1 = st.radio(
        "1. Which type of database stores data in tables?", 
        ["MongoDB", "MySQL", "Firebase", "None"], 
        index=None
    )
    if q1:
        if q1 == "MySQL":
            st.success("✅ Correct! MySQL is a relational database.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q2 = st.radio(
        "2. In MongoDB, data is stored as?", 
        ["Tables", "Rows", "Documents", "Spreadsheets"], 
        index=None
    )
    if q2:
        if q2 == "Documents":
            st.success("✅ Correct! MongoDB stores data as JSON-like documents.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q3 = st.radio(
        "3. What does CRUD stand for?", 
        ["Create, Read, Update, Delete", 
         "Copy, Run, Upload, Download", 
         "Connect, Render, Update, Debug"], 
        index=None
    )
    if q3:
        if q3 == "Create, Read, Update, Delete":
            st.success("✅ Correct! That's CRUD.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    # Show results when all answered
    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {score}/3")
        if score >= 2:  # passing condition
            if "quiz4_done" not in st.session_state:  # prevent multiple XP gains
                st.session_state.xp += 10
                st.session_state.quiz4_done = True

                # 🔑 Mark Chapter 1 as completed
                st.session_state.completed_chapters.add(4)
                save_progress()
            st.success("🏆 Great job! You earned +10 XP.")
            save_progress()
        else:
            st.warning("⚠️ You scored less than 2. Try again to earn XP.")

elif chapter == "Chapter 4 Tasks":
    st.header("📝 Chapter 4 Tasks: Databases & MongoDB")
    st.write("These tasks will help you practice CRUD and MongoDB concepts.")

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Create a MongoDB document for a `book`:
       - Fields: `title`, `author`, `year`.

    2. Insert 3 user documents into a `users` collection:
       - Example: `{ "name": "Ali", "email": "ali@example.com" }`

    3. Write a query to **find all users** with `age > 20`.

    4. Update a user's email from `old@example.com` to `new@example.com`.

    5. Delete one document from the `users` collection.
    """)

elif chapter == "Chapter 5: REST APIs":
    st.header("🌐 Chapter 5: REST APIs (Representational State Transfer)")
    chapter_divider(5)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    REST API is a way for applications to **communicate over the web** using rules (HTTP methods).  
    It’s how the frontend (React, Angular, etc.) talks to the backend (Node.js, Express, etc.).

    ### 🔑 Key Concepts:
    - **Client & Server** → Client (browser, app) sends requests, Server responds.
    - **HTTP Methods**:
        - `GET` → Fetch data  
        - `POST` → Send new data  
        - `PUT` → Update existing data  
        - `DELETE` → Remove data  

    - **Endpoints** → URLs used to access resources.  
      Example:  
      - `/users` → list all users  
      - `/users/1` → get user with ID=1  

    - **Request & Response**:
        - **Request** contains → method, URL, body, headers  
        - **Response** contains → status code, message, data  

    - **CRUD Operations** map to HTTP:
        - Create → `POST`
        - Read → `GET`
        - Update → `PUT`
        - Delete → `DELETE`

    ### 🚀 Example Use Case:
    Imagine an **online shop**:  
    - `GET /products` → Fetch all products  
    - `POST /products` → Add new product  
    - `PUT /products/2` → Update product with ID=2  
    - `DELETE /products/3` → Remove product with ID=3  

    ### 🧠 Why REST APIs?
    - Frontend & backend stay separate.  
    - APIs make apps **scalable** (can be used on mobile, web, IoT).  
    - Standard communication method.
    """)

    st.subheader("📊 REST API Workflow Diagram")
    st.markdown("""
    ```
    [ Client (Browser/Mobile) ] 
               │
               ▼
        [ REST API (Server) ] 
               │
               ▼
        [ Database (MongoDB/MySQL) ]
    ```
    """)

    st.subheader("📺 Learn More (Hindi Tutorial)")
    st.video("https://www.youtube.com/watch?v=mqm4QPEwtZQ")  # REST API Hindi tutorial


elif chapter == "Chapter 5 Quiz":
    st.header("🧩 Chapter 5 Quiz: REST APIs")

    score = 0

    q1 = st.radio("1. Which HTTP method is used to fetch data from a server?", 
                  ["POST", "GET", "PUT", "DELETE"], index=None)
    if q1:
        if q1 == "GET":
            st.success("✅ Correct! GET is used to retrieve data.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q2 = st.radio("2. Which HTTP method is used to update existing data?", 
                  ["POST", "PUT", "DELETE", "GET"], index=None)
    if q2:
        if q2 == "PUT":
            st.success("✅ Correct! PUT updates data.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q3 = st.radio("3. What does an API endpoint represent?", 
                  ["A database table", "A file path", "A URL to access a resource", "A server password"], index=None)
    if q3:
        if q3 == "A URL to access a resource":
            st.success("✅ Correct! Endpoints are URLs for accessing resources.")
            score += 1
        else:
            st.error("❌ Try again!")

    q4 = st.radio("4. Which status code means 'Success' in REST API?", 
                  ["200", "404", "500", "302"], index=None)
    if q4:
        if q4 == "200":
            st.success("✅ Correct! 200 means success.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q5 = st.radio("5. CRUD operation 'Delete' is mapped to which HTTP method?", 
                  ["GET", "POST", "DELETE", "PUT"], index=None)
    if q5:
        if q5 == "DELETE":
            st.success("✅ Correct! DELETE removes a resource.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    # Show results after all answered
    if q1 and q2 and q3 and q4 and q5:
        st.subheader(f"📊 Score: {score}/5")
        if score >= 3:  # passing condition
            if "quiz5_done" not in st.session_state:
                st.session_state.xp += 10
                st.session_state.quiz5_done = True

                # 🔑 Mark Chapter 1 as completed
                st.session_state.completed_chapters.add(5)
                save_progress()
            st.success("🏆 Great job! You earned +10 XP.")
        else:
            st.warning("⚠️ Score less than 3. Try again to earn XP.")
 

elif chapter == "Chapter 5 Tasks":
    st.header("📝 Chapter 5 Tasks: REST APIs")
    st.write("""
    These tasks will help you practice building and using REST APIs.
    """)

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Create a Node.js/Express API with one route:
       - `GET /hello` → returns "Hello API World".

    2. Add a new route:
       - `GET /time` → returns the current server time in JSON format.

    3. Build a small "To-Do API":
       - `GET /todos` → returns a list of tasks (array).  
       - `POST /todos` → allows adding a new task.  

    4. Add error handling:
       - If a wrong route is called, return a 404 JSON response:
         ```json
         { "error": "Route not found" }
         ```

    5. Bonus Challenge 🚀:
       - Create a "Users API" with routes:
         - `GET /users` → returns list of users.  
         - `GET /users/:id` → returns user details by ID.  
         - `POST /users` → adds a new user.  
    """)

elif chapter == "Chapter 6: Authentication & Security":
    st.header("🔐 Chapter 6: Authentication & Security")
    chapter_divider(6)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    In any backend system, **security** is extremely important.  
    Authentication ensures that only the **right users** can access your application.  

    ### 🔑 Key Concepts:
    - **Authentication** → Verifying *who* the user is (e.g., login with username & password).  
    - **Authorization** → Verifying *what* the user is allowed to do (e.g., admin vs normal user).  
    - **Hashing Passwords** → Passwords should never be stored as plain text.  
    - **JWT (JSON Web Tokens)** → A secure way to store user identity across requests.  

    Example flow:
    1. User logs in with username & password.  
    2. Backend checks the password (hashed).  
    3. If correct → backend creates a **JWT token** and sends it to the user.  
    4. The user includes the token in every request → proves they are logged in.  
    """)

    st.subheader("🧑‍💻 Example Code: Hashing Passwords in Python")
    st.code("""
import hashlib

# User signup → hash password before saving
password = "mypassword123"
hashed_pw = hashlib.sha256(password.encode()).hexdigest()
print("Stored password (hashed):", hashed_pw)

# User login → hash input again and compare
login_input = "mypassword123"
if hashlib.sha256(login_input.encode()).hexdigest() == hashed_pw:
    print("✅ Login successful")
else:
    print("❌ Invalid password")
""", language="python")

    st.subheader("🧑‍💻 Example Code: Simple JWT in Node.js")
    st.code("""
const jwt = require("jsonwebtoken");

// User object
const user = { id: 1, username: "john_doe" };

// Generate JWT
const token = jwt.sign(user, "secretKey", { expiresIn: "1h" });
console.log("Generated Token:", token);

// Verify JWT
jwt.verify(token, "secretKey", (err, decoded) => {
    if (err) console.log("❌ Invalid token");
    else console.log("✅ Verified user:", decoded);
});
""", language="javascript")
    st.write("...your explanation content here...")
    st.subheader("📺 Learn More (Coding in Hindi)")
    st.video("https://www.youtube.com/watch?v=IWmIi6E1IAI") 
     # JWT tutorial in Hindi

elif chapter == "Chapter 6 Quiz":
    st.header("🧩 Chapter 6 Quiz: Authentication & Security")

    score = 0

    q1 = st.radio("1. What does authentication mean?", 
                  ["Verifying user identity", "Encrypting data", "Building APIs", "Managing servers"], index=None)
    if q1:
        if q1 == "Verifying user identity":
            st.success("✅ Correct! Authentication is about verifying who the user is.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q2 = st.radio("2. Which of these is NOT an authentication method?", 
                  ["Password", "OAuth", "JWT", "CSS"], index=None)
    if q2:
        if q2 == "CSS":
            st.success("✅ Correct! CSS is for styling, not authentication.")
            score += 1
            save_progress()

        else:
            st.error("❌ Try again!")

    q3 = st.radio("3. What does JWT stand for?", 
                  ["Java Web Token", "JSON Web Token", "JavaScript With Token", "Join Web Transfer"], index=None)
    if q3:
        if q3 == "JSON Web Token":
            st.success("✅ Correct! JWT = JSON Web Token.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q4 = st.radio("4. What is the main purpose of hashing passwords?", 
                  ["To store them safely", "To make them look fancy", "To speed up login", "To create tokens"], index=None)
    if q4:
        if q4 == "To store them safely":
            st.success("✅ Correct! Hashing makes passwords secure in databases.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q5 = st.radio("5. In OAuth, which service is commonly used for login?", 
                  ["Facebook/Google", "VS Code", "Excel", "MongoDB"], index=None)
    if q5:
        if q5 == "Facebook/Google":
            st.success("✅ Correct! OAuth allows login with Google, Facebook, etc.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    # Show results after all answered
    if q1 and q2 and q3 and q4 and q5:
        st.subheader(f"📊 Score: {score}/5")
        if score >= 3:  # passing condition
            if "quiz6_done" not in st.session_state:
                st.session_state.xp += 10
                st.session_state.quiz6_done = True

                # 🔑 Mark Chapter 1 as completed
                st.session_state.completed_chapters.add(6)
                save_progress()
            st.success("🏆 Great job! You earned +10 XP.")

        else:
            st.warning("⚠️ Score less than 3. Try again to earn XP.")


elif chapter == "Chapter 6 Tasks":
    st.header("📝 Chapter 6 Tasks: Authentication & Security")
    st.write("Practice real authentication & security concepts with these tasks.")

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Create a **Node.js login system** that:
       - Takes a username & password as input.  
       - Prints `"Login successful"` if correct, otherwise `"Login failed"`.  

    2. Hash a password using **bcrypt**:
       - Install bcrypt (`npm install bcrypt`).  
       - Hash the password `"mypassword"`.  
       - Print the hashed value.  

    3. Generate a **JWT token**:
       - Install `jsonwebtoken`.  
       - Create a token with `{ user: "John" }`.  
       - Print the token.  

    4. Verify a **JWT token**:
       - Decode and verify the token you generated.  
       - Print `"Valid user"` if verified.  

    5. Create a **middleware** in Express.js:
       - It should check if a user provides a valid token in the request header.  
       - If valid → allow access.  
       - If not → return `"Access Denied"`.  

    6. Build a **secure API endpoint** `/profile`:
       - Only accessible if the user is logged in with a valid token.  
       - Otherwise return an error.  
    """)



elif chapter == "Chapter 7: REST APIs & CRUD (Deep)":
    st.header("🌐 Chapter 7: REST APIs & CRUD Operations (Deep Dive)")
    chapter_divider(7)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    Now that you know the basics of REST APIs, let’s go deeper:  

    1. **REST Principles**  
       - Stateless → Every request contains all the info (server does not remember state).  
       - Resource-based → APIs expose "resources" like `/users`, `/products`.  
       - Uses HTTP Methods:  
         - `GET` → Read  
         - `POST` → Create  
         - `PUT` → Update  
         - `DELETE` → Delete  

    2. **Error Handling**  
       APIs should return proper status codes like:  
       - 200 → OK  
       - 201 → Created  
       - 400 → Bad Request  
       - 404 → Not Found  
       - 500 → Server Error  

    3. **Using MongoDB with CRUD**  
       Instead of keeping data in memory, let’s connect Express.js with MongoDB.
    """)

    st.subheader("💻 Example Code: Express.js + MongoDB CRUD API")

    st.code("""
    const express = require('express');
    const mongoose = require('mongoose');
    const app = express();
    const port = 4000;

    app.use(express.json());

    // MongoDB connection
    mongoose.connect('mongodb://localhost:27017/backend_course', {
        useNewUrlParser: true,
        useUnifiedTopology: true
    }).then(() => console.log("✅ Connected to MongoDB"))
      .catch(err => console.log("❌ DB Error:", err));

    // Define Schema
    const userSchema = new mongoose.Schema({
        name: String,
        email: String
    });

    const User = mongoose.model('User', userSchema);

    // CREATE
    app.post('/users', async (req, res) => {
        try {
            const user = new User(req.body);
            await user.save();
            res.status(201).json(user);
        } catch (err) {
            res.status(400).json({ error: err.message });
        }
    });

    // READ all
    app.get('/users', async (req, res) => {
        const users = await User.find();
        res.json(users);
    });

    // READ by ID
    app.get('/users/:id', async (req, res) => {
        try {
            const user = await User.findById(req.params.id);
            if (!user) return res.status(404).json({ message: "User not found" });
            res.json(user);
        } catch (err) {
            res.status(400).json({ error: err.message });
        }
    });

    // UPDATE
    app.put('/users/:id', async (req, res) => {
        try {
            const user = await User.findByIdAndUpdate(req.params.id, req.body, { new: true });
            if (!user) return res.status(404).json({ message: "User not found" });
            res.json(user);
        } catch (err) {
            res.status(400).json({ error: err.message });
        }
    });

    // DELETE
    app.delete('/users/:id', async (req, res) => {
        try {
            const user = await User.findByIdAndDelete(req.params.id);
            if (!user) return res.status(404).json({ message: "User not found" });
            res.json({ message: "User deleted" });
        } catch (err) {
            res.status(400).json({ error: err.message });
        }
    });

    app.listen(port, () => {
        console.log(`🚀 API running at http://localhost:${port}`);
    });
    """, language="javascript")

    st.success("👉 This version stores users in **MongoDB** instead of memory, making it more realistic!")
    st.write("...your explanation content here...")
    st.subheader("📺 Learn More (Coding in Hindi)")
    st.video("https://www.youtube.com/watch?v=09_SDJ2au6E") 


elif chapter == "Chapter 7 Quiz":
    st.header("🧩 Chapter 7 Quiz: REST APIs & CRUD (Deep Dive)")

    score = 0

    q1 = st.radio("1. What does CRUD stand for?", 
                  ["Create, Read, Update, Delete", 
                   "Connect, Run, Upload, Download", 
                   "Copy, Reset, Undo, Drop"], index=None)
    if q1:
        if q1 == "Create, Read, Update, Delete":
            st.success("✅ Correct! That’s the CRUD cycle.")
            score += 1
        else:
            st.error("❌ Try again!")

    q2 = st.radio("2. In REST API design, which HTTP method is used to update a resource?", 
                  ["GET", "POST", "PUT/PATCH", "DELETE"], index=None)
    if q2:
        if q2 == "PUT/PATCH":
            st.success("✅ Correct! PUT/PATCH is used for updating resources.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q3 = st.radio("3. Which HTTP status code means 'Resource Created Successfully'?", 
                  ["200 OK", "201 Created", "404 Not Found", "500 Internal Server Error"], index=None)
    if q3:
        if q3 == "201 Created":
            st.success("✅ Correct! 201 is returned when a resource is created.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q4 = st.radio("4. In REST, data is usually exchanged in which format?", 
                  ["CSV", "XML", "JSON", "Excel"], index=None)
    if q4:
        if q4 == "JSON":
            st.success("✅ Correct! JSON is the most common format.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q5 = st.radio("5. Which of these routes is RESTful for getting a single user with id=5?", 
                  ["/getUser?id=5", "/users/5", "/fetch-user/5", "/find-user?id=5"], index=None)
    if q5:
        if q5 == "/users/5":
            st.success("✅ Correct! That’s a RESTful way to design routes.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q6 = st.radio("6. Which tool is commonly used for testing REST APIs?", 
                  ["PowerPoint", "Photoshop", "Postman", "Notepad"], index=None)
    if q6:
        if q6 == "Postman":
            st.success("✅ Correct! Postman is the most popular API testing tool.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q7 = st.radio("7. In MongoDB with Express, which function is used to find all documents?", 
                  ["find()", "findOne()", "getAll()", "search()"], index=None)
    if q7:
        if q7 == "find()":
            st.success("✅ Correct! `find()` retrieves all documents.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    # Show results once all answered
    if q1 and q2 and q3 and q4 and q5 and q6 and q7:
        st.subheader(f"📊 Score: {score}/7")
        if score >= 4:  # passing condition
            if "quiz7_done" not in st.session_state:
                st.session_state.xp += 10
                st.session_state.quiz7_done = True

                # 🔑 Mark Chapter 1 as completed
                st.session_state.completed_chapters.add(7)
                save_progress()
            st.success("🏆 Great job! You earned +10 XP.")
        else:
            st.warning("⚠️ Score less than 4. Try again to earn XP.")

elif chapter == "Chapter 7 Tasks":
    st.header("📝 Chapter 7 Tasks: REST APIs & CRUD")

    st.write("""
    In this chapter, you’ll practice creating and testing REST APIs using Node.js + Express + MongoDB.  
    Try solving these tasks step by step. Each builds on the previous one. 🚀
    """)

    task = st.radio("Choose a task to view:", 
                    ["Task 1: Build a Simple API",
                     "Task 2: Add CRUD Operations",
                     "Task 3: Use RESTful Routes",
                     "Task 4: Connect to MongoDB",
                     "Task 5: Implement Error Handling",
                     "Task 6: Bonus Challenge – User API"], index=None)

    if task == "Task 1: Build a Simple API":
        st.subheader("🚀 Task 1: Build a Simple API")
        st.write("""
        - Create a new Express.js project.
        - Add a single route: `/` that returns `"Hello Backend!"`.
        - Run the server and test it in your browser or Postman.
        """)

    elif task == "Task 2: Add CRUD Operations":
        st.subheader("🛠️ Task 2: Add CRUD Operations")
        st.write("""
        - Create a new route `/books`.
        - Add the following routes:
          - `GET /books` → Return all books (array).
          - `POST /books` → Add a new book.
          - `PUT /books/:id` → Update a book by ID.
          - `DELETE /books/:id` → Delete a book by ID.
        """)

    elif task == "Task 3: Use RESTful Routes":
        st.subheader("📡 Task 3: Use RESTful Routes")
        st.write("""
        - Update your routes to follow REST conventions.
        - Example:
          - `GET /users` → Get all users
          - `GET /users/:id` → Get one user
          - `POST /users` → Add a user
          - `PUT /users/:id` → Update a user
          - `DELETE /users/:id` → Remove a user
        """)

    elif task == "Task 4: Connect to MongoDB":
        st.subheader("💾 Task 4: Connect to MongoDB")
        st.write("""
        - Install `mongoose` (`npm install mongoose`).
        - Connect your project to MongoDB (local or Atlas).
        - Define a `Book` schema with title, author, year.
        - Modify your `/books` routes to use MongoDB instead of arrays.
        """)

    elif task == "Task 5: Implement Error Handling":
        st.subheader("⚠️ Task 5: Implement Error Handling")
        st.write("""
        - Add proper error handling for:
          - Invalid IDs
          - Missing data in POST
          - Database errors
        - Return correct HTTP status codes (400, 404, 500).
        """)

    elif task == "Task 6: Bonus Challenge – User API":
        st.subheader("🏆 Task 6: Bonus Challenge – User API")
        st.write("""
        - Build a `User` API with fields: name, email, password.
        - Add CRUD routes for users.
        - Add validation: email must be unique.
        - Optional: Add password hashing with `bcrypt`.
        """)
elif chapter == "Final Project: Chapters 1–7":
    st.header("🚀 Final Project: Backend from Scratch")

    st.write("""
    Now it’s time to put together everything you learned from **Chapter 1 → 7**.  
    This will be your **capstone project**, covering backend concepts, Node.js, Express, MongoDB, REST APIs, and more.  

    You don’t need to finish it all at once. Do it step by step. ✨
    """)

    project = st.radio("Choose a project challenge:", 
                       ["Project 1: Book Management System",
                        "Project 2: Notes API with Authentication",
                        "Project 3: Student Management System",
                        "Project 4: Blog Platform (Bonus)"], index=None)

    if project == "Project 1: Book Management System":
        st.subheader("📚 Project 1: Book Management System")
        st.write("""
        - Build a complete **Book API** using Node.js + Express + MongoDB.  
        - Features:
          - `POST /books` → Add a new book.
          - `GET /books` → Get all books.
          - `GET /books/:id` → Get one book.
          - `PUT /books/:id` → Update book details.
          - `DELETE /books/:id` → Delete a book.
        - Extra: Add error handling, and return JSON responses with proper status codes.
        """)

    elif project == "Project 2: Notes API with Authentication":
        st.subheader("📝 Project 2: Notes API with Authentication")
        st.write("""
        - Create a **Notes App Backend**.
        - Features:
          - Users can sign up and log in (`POST /signup`, `POST /login`).
          - Use **JWT (JSON Web Token)** for authentication.
          - Authenticated users can:
            - `POST /notes` → Add a note.
            - `GET /notes` → See all their notes.
            - `PUT /notes/:id` → Edit their note.
            - `DELETE /notes/:id` → Delete their note.
        - Extra: Add password hashing using `bcrypt`.
        """)

    elif project == "Project 3: Student Management System":
        st.subheader("🎓 Project 3: Student Management System")
        st.write("""
        - Create a backend for a **Student Management App**.
        - Features:
          - `POST /students` → Add new student (name, age, class).
          - `GET /students` → List all students.
          - `GET /students/:id` → Get one student.
          - `PUT /students/:id` → Update student.
          - `DELETE /students/:id` → Remove student.
        - Extra: Add validations (e.g., age must be a number).
        """)

    elif project == "Project 4: Blog Platform (Bonus)":
        st.subheader("✍️ Project 4: Blog Platform (Bonus)")
        st.write("""
        - Build a **Blog API** where users can:
          - Register & log in.
          - Create, read, update, and delete blog posts.
          - Comment on blog posts.
        - Use MongoDB for storing users, posts, and comments.
        - Add authentication and error handling.
        """)

elif chapter == "Chapter 8: Deployment & Hosting":
    st.header("🚀 Chapter 8: Deployment & Hosting")
    chapter_divider(8)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    After building your backend, the next step is to **deploy it online** so others can access it.  

    Common platforms:
    - **Render** → Free & easy for Node.js apps
    - **Railway** → Free plan, simple deployment
    - **Heroku** → Popular, supports Node.js & MongoDB
    - **Vercel** → Mainly for frontend but can deploy APIs
    """)

    st.subheader("💻 Example: Prepare Node.js App for Deployment")
    st.code("""
    // 1. Ensure you have a package.json with start script
    "scripts": {
        "start": "node index.js"
    }

    // 2. Use environment variables for sensitive info
    const express = require('express');
    const mongoose = require('mongoose');
    require('dotenv').config();  // npm install dotenv

    const app = express();
    const port = process.env.PORT || 3000;

    mongoose.connect(process.env.MONGO_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    }).then(() => console.log("✅ Connected to MongoDB"))
      .catch(err => console.log("❌ DB Error:", err));

    app.get('/', (req, res) => {
        res.send("Hello, deployed backend!");
    });

    app.listen(port, () => console.log(`Server running on port ${port}`));
    """, language="javascript")

    st.subheader("📦 Steps to Deploy on Render (Example)")
    st.markdown("""
    1. Push your project to **GitHub**.
    2. Go to [Render](https://render.com) → New → Web Service.
    3. Connect your GitHub repo.
    4. Set build command: `npm install`.
    5. Set start command: `npm start`.
    6. Add **environment variables** (like `MONGO_URI`) in Render dashboard.
    7. Click deploy → Your backend will be online!
    """)

    st.subheader("📺 Optional Video Tutorial (Hindi)")
    st.video("https://www.youtube.com/watch?v=PKpF7nJ9Y1M")  # Example Render deployment tutorial

elif chapter == "Chapter 8 Quiz":
    st.header("🧩 Chapter 8 Quiz: Deployment & Hosting")

    score = 0

    q1 = st.radio("1. Which command is commonly used to start a Node.js server in production?", 
                  ["node index.js", "npm install", "npm start", "npm run test"], index=None)
    if q1:
        if q1 == "npm start":
            st.success("✅ Correct! `npm start` runs the start script in package.json.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q2 = st.radio("2. What is the purpose of environment variables in deployment?", 
                  ["To store sensitive info like DB credentials", 
                   "To store app styling", 
                   "To increase server speed", 
                   "To debug code"], index=None)
    if q2:
        if q2 == "To store sensitive info like DB credentials":
            st.success("✅ Correct! Environment variables keep secrets safe.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q3 = st.radio("3. Which platform can you use to deploy Node.js apps for free?", 
                  ["Render", "Railway", "Heroku", "All of the above"], index=None)
    if q3:
        if q3 == "All of the above":
            st.success("✅ Correct! All three offer free deployment options.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q4 = st.radio("4. What should you do if your app needs a database connection in deployment?", 
                  ["Hardcode credentials", "Use environment variables", "Use local files only", "Ignore"], index=None)
    if q4:
        if q4 == "Use environment variables":
            st.success("✅ Correct! Never hardcode credentials.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q5 = st.radio("5. Which file usually contains the start command for Node.js apps?", 
                  ["package.json", "index.js", ".env", "README.md"], index=None)
    if q5:
        if q5 == "package.json":
            st.success("✅ Correct! package.json has scripts including start.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    # Show results once all answered
    if q1 and q2 and q3 and q4 and q5:
        st.subheader(f"📊 Score: {score}/5")
        if score >= 3:
            if "quiz8_done" not in st.session_state:
                st.session_state.xp += 10
                st.session_state.quiz8_done = True

                # 🔑 Mark Chapter 1 as completed
                st.session_state.completed_chapters.add(8)
                save_progress()
            st.success("🏆 Great job! You earned +10 XP.")
        else:
            st.warning("⚠️ Score less than 3. Try again to earn XP.")

elif chapter == "Chapter 8 Tasks":
    st.header("📝 Chapter 8 Tasks: Deployment & Hosting")

    st.write("""
    Practice deploying your backend app with these tasks. Start simple, then advance. 🚀
    """)

    task = st.radio("Choose a deployment task:", 
                    ["Task 1: Prepare Local Node.js App",
                     "Task 2: Add Environment Variables",
                     "Task 3: Deploy on Render",
                     "Task 4: Deploy on Railway",
                     "Task 5: Test Your Deployed API"], index=None)

    if task == "Task 1: Prepare Local Node.js App":
        st.subheader("🛠️ Task 1: Prepare Local Node.js App")
        st.write("""
        - Ensure your app has `package.json` with a start script.  
        - Test your app locally: `npm install` → `npm start`.  
        - Check all routes are working.  
        """)

    elif task == "Task 2: Add Environment Variables":
        st.subheader("🔐 Task 2: Add Environment Variables")
        st.write("""
        - Create a `.env` file.  
        - Add `PORT=3000` and `MONGO_URI=<your_mongo_url>`.  
        - Use `process.env.PORT` and `process.env.MONGO_URI` in your code.  
        - Test that the app works with the environment variables.  
        """)

    elif task == "Task 3: Deploy on Render":
        st.subheader("🚀 Task 3: Deploy on Render")
        st.write("""
        - Push your project to **GitHub**.  
        - Go to [Render](https://render.com) → New → Web Service.  
        - Connect your GitHub repo, set build/start commands.  
        - Add environment variables.  
        - Deploy and test your API online.  
        """)

    elif task == "Task 4: Deploy on Railway":
        st.subheader("🌐 Task 4: Deploy on Railway")
        st.write("""
        - Sign up on [Railway](https://railway.app).  
        - Import your GitHub repo.  
        - Set environment variables and deploy.  
        - Test all routes of your API.  
        """)

    elif task == "Task 5: Test Your Deployed API":
        st.subheader("✅ Task 5: Test Your Deployed API")
        st.write("""
        - Use **Postman** or **curl** to test all endpoints.  
        - Verify CRUD operations or authentication work as expected.  
        - Optional: Share your deployed API link with a friend to test it.  
        """)

elif chapter == "Chapter 9: Advanced Backend Concepts (Deep)":
    st.header("⚡ Chapter 9: Advanced Backend Concepts & Optimization (Deep Dive)")
    chapter_divider(9)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    In this chapter, you’ll learn advanced techniques to build **production-ready backends**:
    - Middleware chaining & modularization  
    - Advanced error handling  
    - Caching with Redis  
    - Logging with Winston  
    - Performance & scalability tips  
    - Environment-based configuration
    """)

    st.subheader("1️⃣ Modular Middleware")
    st.write("""
    Split middleware into modules for **clean code** and reusability.
    """)
    st.code("""
    // authMiddleware.js
    module.exports = (req, res, next) => {
        if(!req.headers.authorization){
            return res.status(401).json({ error: 'Unauthorized' });
        }
        next();
    };

    // index.js
    const express = require('express');
    const auth = require('./authMiddleware');
    const app = express();

    app.get('/protected', auth, (req, res) => {
        res.send('You passed the auth middleware!');
    });
    """, language="javascript")

    st.subheader("2️⃣ Advanced Caching with Redis")
    st.write("""
    Use **Redis** for caching API responses for fast access and scalability.
    """)
    st.code("""
    const redis = require('redis');
    const client = redis.createClient();

    app.get('/data/:id', async (req, res) => {
        const id = req.params.id;
        client.get(id, async (err, cachedData) => {
            if(cachedData) return res.json({ data: JSON.parse(cachedData), cached: true });

            const dbData = { id: id, value: 'Fetched from DB' }; // Simulate DB
            client.setex(id, 3600, JSON.stringify(dbData)); // Cache for 1 hour
            res.json({ data: dbData, cached: false });
        });
    });
    """, language="javascript")

    st.subheader("3️⃣ Advanced Logging with Winston")
    st.write("""
    Use **Winston** to log info, warnings, and errors to files or external services.
    """)
    st.code("""
    const winston = require('winston');

    const logger = winston.createLogger({
        level: 'info',
        format: winston.format.json(),
        transports: [
            new winston.transports.File({ filename: 'error.log', level: 'error' }),
            new winston.transports.File({ filename: 'combined.log' }),
        ],
    });

    app.use((req, res, next) => {
        logger.info(`${req.method} ${req.url}`);
        next();
    });
    """, language="javascript")

    st.subheader("4️⃣ Error Handling & Async Patterns")
    st.write("""
    Handle async routes gracefully and avoid crashing the server.
    """)
    st.code("""
    const asyncHandler = require('express-async-handler');

    app.get('/async-data', asyncHandler(async (req, res, next) => {
        const data = await someAsyncFunction(); // May throw error
        res.json(data);
    }));

    // Global error middleware
    app.use((err, req, res, next) => {
        console.error(err.stack);
        res.status(500).json({ error: err.message || 'Internal Server Error' });
    });
    """, language="javascript")

    st.subheader("5️⃣ Performance & Scalability Tips")
    st.markdown("""
    - Use **indexes** in MongoDB to speed up queries.  
    - Avoid blocking code; use **async/await** everywhere.  
    - Compress responses using **compression** middleware.  
    - Limit request rate with **express-rate-limit**.  
    - Deploy with **PM2** for clustering & monitoring.  
    - Split routes into modules and use `router` for cleaner code.
    """)

elif chapter == "Chapter 9 Quiz":
    st.header("🧩 Chapter 9 Quiz: Authentication & Authorization")

    score = 0

    q1 = st.radio("1. What is the main purpose of authentication?", 
                  ["To verify who the user is", 
                   "To decide what resources a user can access", 
                   "To encrypt database", 
                   "To deploy applications"], index=None)
    if q1:
        if q1 == "To verify who the user is":
            st.success("✅ Correct! Authentication checks identity (e.g., login).")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q2 = st.radio("2. Authorization is mainly about:", 
                  ["Verifying user identity", 
                   "Granting or denying access to resources", 
                   "Encrypting API requests", 
                   "Database optimization"], index=None)
    if q2:
        if q2 == "Granting or denying access to resources":
            st.success("✅ Correct! Authorization controls access after authentication.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q3 = st.radio("3. Which standard is commonly used for secure authentication?", 
                  ["OAuth2", "CSS", "HTML", "Excel"], index=None)
    if q3:
        if q3 == "OAuth2":
            st.success("✅ Correct! OAuth2 is widely used for secure authentication.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q4 = st.radio("4. What is JWT commonly used for?", 
                  ["Frontend styling", 
                   "User session tokens", 
                   "Database indexing", 
                   "File storage"], index=None)
    if q4:
        if q4 == "User session tokens":
            st.success("✅ Correct! JWT stores user identity securely in tokens.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q5 = st.radio("5. Which one is an example of Multi-Factor Authentication (MFA)?", 
                  ["Password only", 
                   "Password + OTP", 
                   "Username only", 
                   "API key only"], index=None)
    if q5:
        if q5 == "Password + OTP":
            st.success("✅ Correct! MFA combines multiple verification methods.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    # Show score only when all answered
    if q1 and q2 and q3 and q4 and q5:
        st.subheader(f"📊 Score: {score}/5")
        if score >= 3:
            st.session_state.xp += 10
            st.success("🏆 Great job! You earned +10 XP.")

            # 🔑 Mark Chapter 1 as completed
            st.session_state.completed_chapters.add(9)
            save_progress()
        else:
            st.warning("⚠️ Score less than 3. Try again to earn XP.")


elif chapter == "Chapter 9 Tasks":
    st.header("📝 Chapter 9 Tasks: Advanced Backend Concepts")

    st.write("""
    Practice advanced backend concepts with these tasks. Try implementing them step by step.
    """)

    task = st.radio("Choose a task:", 
                    ["Task 1: Modular Middleware",
                     "Task 2: Redis Caching",
                     "Task 3: Winston Logging",
                     "Task 4: Async Error Handling",
                     "Task 5: Performance Optimization Challenge"], index=None)

    if task == "Task 1: Modular Middleware":
        st.subheader("🔧 Task 1: Modular Middleware")
        st.write("""
        - Create an `authMiddleware.js` to check headers for authorization.  
        - Import it in your main app and protect `/protected` route.  
        - Test that unauthorized requests get 401 status.  
        """)

    elif task == "Task 2: Redis Caching":
        st.subheader("⚡ Task 2: Redis Caching")
        st.write("""
        - Install Redis and `redis` npm package.  
        - Cache responses for `/data/:id` route for 1 hour.  
        - Test that repeated requests return cached data (cached: true).  
        """)

    elif task == "Task 3: Winston Logging":
        st.subheader("📄 Task 3: Winston Logging")
        st.write("""
        - Install Winston.  
        - Log all incoming requests to `combined.log`.  
        - Log only errors to `error.log`.  
        - Test by making a route that throws an error.  
        """)

    elif task == "Task 4: Async Error Handling":
        st.subheader("💥 Task 4: Async Error Handling")
        st.write("""
        - Wrap async routes using `express-async-handler`.  
        - Create a route `/async-error` that throws an error asynchronously.  
        - Verify the global error middleware catches it and returns 500.  
        """)

    elif task == "Task 5: Performance Optimization Challenge":
        st.subheader("🚀 Task 5: Performance Optimization Challenge")
        st.write("""
        - Add **compression** middleware to compress responses.  
        - Add **rate-limiting** middleware using `express-rate-limit`.  
        - Ensure MongoDB queries use **indexes** for fast retrieval.  
        - Test performance with Postman or Apache Bench (`ab`) tool.  
        """)

elif chapter == "Chapter 10: Microservices":
    st.header("⚡ Chapter 10: Microservices & Advanced Backend Architecture")
    chapter_divider(10)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    In large-scale applications, a **monolithic backend** becomes hard to manage.  
    Microservices allow you to split your backend into **small, independent services** that communicate over APIs.  

    Key concepts:
    - Each service has its own database and API.
    - Services communicate via **HTTP REST** or **message queues**.
    - Easier to scale, deploy, and maintain.
    """)

    st.subheader("1️⃣ Simple Microservice Example")
    st.write("""
    Create **two services**: Users service and Orders service.  
    Each service runs on a different port and communicates via HTTP requests.
    """)

    st.code("""
    // users-service/index.js
    const express = require('express');
    const app = express();
    const users = [{ id:1, name: 'Alice' }];

    app.get('/users', (req, res) => res.json(users));

    app.listen(3001, () => console.log('Users service running on port 3001'));
    """, language="javascript")

    st.code("""
    // orders-service/index.js
    const express = require('express');
    const axios = require('axios');
    const app = express();
    const orders = [{ id:1, userId:1, item: 'Book' }];

    app.get('/orders', async (req, res) => {
        const users = await axios.get('http://localhost:3001/users');
        const ordersWithUser = orders.map(order => {
            const user = users.data.find(u => u.id === order.userId);
            return { ...order, user: user.name };
        });
        res.json(ordersWithUser);
    });

    app.listen(3002, () => console.log('Orders service running on port 3002'));
    """, language="javascript")

    st.subheader("2️⃣ Service Communication")
    st.markdown("""
    - Orders service requests user info from Users service using **HTTP GET**.  
    - In real-world, you might use **message queues** like RabbitMQ or Kafka for async communication.
    """)

    st.subheader("3️⃣ Environment & Configuration")
    st.markdown("""
    - Each service should use its **own `.env` file** for sensitive info.  
    - Example:
      - USERS_PORT=3001  
      - ORDERS_PORT=3002  
      - DATABASE_URL=<mongo_connection>
    """)

    st.subheader("4️⃣ Scaling Microservices")
    st.markdown("""
    - You can deploy each service independently.  
    - Use **Docker** to containerize services.  
    - Use **load balancers** to distribute traffic.  
    - Monitor each service individually for performance.
    """)

elif chapter == "Chapter 10 Quiz":
    st.header("🧩 Chapter 10 Quiz: Microservices & Advanced Backend Architecture")

    score = 0

    q1 = st.radio("1. What is the main advantage of microservices over monolithic architecture?", 
                  ["Easier scaling and maintenance", 
                   "Faster frontend rendering", 
                   "Less coding required", 
                   "Automatic database backups"], index=None)
    if q1:
        if q1 == "Easier scaling and maintenance":
            st.success("✅ Correct! Microservices allow independent scaling and deployment.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q2 = st.radio("2. How do microservices usually communicate?", 
                  ["HTTP REST, message queues, gRPC", 
                   "CSS and HTML", 
                   "Direct DB file access", 
                   "Static text files"], index=None)
    if q2:
        if q2 == "HTTP REST, message queues, gRPC":
            st.success("✅ Correct! Services communicate over network protocols.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q3 = st.radio("3. Why should each microservice have its own database?", 
                  ["To decouple services and avoid single point of failure", 
                   "To use more storage", 
                   "To make frontend faster", 
                   "To confuse developers"], index=None)
    if q3:
        if q3 == "To decouple services and avoid single point of failure":
            st.success("✅ Correct! Each service is independent.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q4 = st.radio("4. What tool is commonly used to containerize microservices?", 
                  ["Docker", "Redis", "Express", "Postman"], index=None)
    if q4:
        if q4 == "Docker":
            st.success("✅ Correct! Docker helps deploy isolated containers.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q5 = st.radio("5. What is a common pattern for async communication between microservices?", 
                  ["Message queues like RabbitMQ or Kafka", 
                   "HTTP GET only", 
                   "Direct DB writes", 
                   "CSS animation"], index=None)
    if q5:
        if q5 == "Message queues like RabbitMQ or Kafka":
            st.success("✅ Correct! Async queues decouple services.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    # Show score only when all answered
    if q1 and q2 and q3 and q4 and q5:
        st.subheader(f"📊 Score: {score}/5")
        if score >= 3:
            st.session_state.xp += 10
            st.success("🏆 Great job! You earned +10 XP.")

                # 🔑 Mark Chapter 1 as completed
            st.session_state.completed_chapters.add(10)
            save_progress()
        else:
            st.warning("⚠️ Score less than 3. Try again to earn XP.")


elif chapter == "Chapter 10 Tasks":
    st.header("📝 Chapter 10 Tasks: Microservices & Advanced Backend Architecture")

    st.write("""
    Practice building microservices and testing communication between them.  
    Start small, then combine multiple services.
    """)

    task = st.radio("Choose a task:", 
                    ["Task 1: Build Users Microservice",
                     "Task 2: Build Orders Microservice",
                     "Task 3: Service Communication",
                     "Task 4: Environment Configuration",
                     "Task 5: Containerize with Docker"], index=None)

    if task == "Task 1: Build Users Microservice":
        st.subheader("👤 Task 1: Build Users Microservice")
        st.write("""
        - Create a new Node.js project for Users service.  
        - Add routes:  
          - `GET /users` → Return a list of users  
          - `POST /users` → Add a user  
        - Run it on port 3001 and test locally.  
        """)

    elif task == "Task 2: Build Orders Microservice":
        st.subheader("🛒 Task 2: Build Orders Microservice")
        st.write("""
        - Create a new Node.js project for Orders service.  
        - Add routes:  
          - `GET /orders` → Return a list of orders  
          - `POST /orders` → Add an order  
        - Run it on port 3002.  
        """)

    elif task == "Task 3: Service Communication":
        st.subheader("🔗 Task 3: Service Communication")
        st.write("""
        - Make Orders service call Users service via HTTP to fetch user details.  
        - Return orders with user info included.  
        - Test that data from both services is combined correctly.  
        """)

    elif task == "Task 4: Environment Configuration":
        st.subheader("⚙️ Task 4: Environment Configuration")
        st.write("""
        - Add `.env` files to both services with separate PORT and DATABASE_URL variables.  
        - Use `process.env` in each service.  
        - Ensure services run correctly with environment variables.  
        """)

    elif task == "Task 5: Containerize with Docker":
        st.subheader("🐳 Task 5: Containerize with Docker")
        st.write("""
        - Write a `Dockerfile` for Users service and another for Orders service.  
        - Build Docker images and run containers locally.  
        - Test that services communicate even when running in containers.  
        - Optional: Use Docker Compose to run both services together.  
        """)

elif chapter == "Chapter 11: Real-Time Backend & WebSockets":
    st.header("⚡ Chapter 11: Real-Time Backend & WebSockets")
    chapter_divider(11)
    # 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    Real-time communication is essential for apps like **chat applications, live notifications, multiplayer games, and stock price updates**.  
    Instead of the client asking the server again and again ("polling"), WebSockets allow a **two-way live connection** between client and server.  

    - **HTTP**: One-way → Client sends request, server responds.  
    - **WebSocket**: Two-way → Both client and server can send data anytime.  

    Common use cases:  
    - 💬 Chat applications  
    - 🔔 Live notifications  
    - 📈 Real-time dashboards  
    - 🎮 Multiplayer games  
    """)

    st.subheader("📜 Example 1: Simple WebSocket Server (Node.js)")
    st.code("""
    // Install: npm install ws
    const WebSocket = require('ws');

    const server = new WebSocket.Server({ port: 8080 });

    server.on('connection', socket => {
        console.log('🔗 New client connected');

        socket.on('message', message => {
            console.log('Received:', message);
            socket.send('Server echo: ' + message);
        });

        socket.on('close', () => {
            console.log('❌ Client disconnected');
        });
    });

    console.log('✅ WebSocket server running on ws://localhost:8080');
    """, language="javascript")

    st.subheader("📜 Example 2: Client Connecting to WebSocket")
    st.code("""
    const socket = new WebSocket("ws://localhost:8080");

    socket.onopen = () => {
        console.log("Connected to server ✅");
        socket.send("Hello from client!");
    };

    socket.onmessage = (event) => {
        console.log("Message from server:", event.data);
    };

    socket.onclose = () => {
        console.log("Disconnected ❌");
    };
    """, language="javascript")

    st.success("With WebSockets, your backend can handle **real-time events** like chat, notifications, and live updates!")

    st.markdown("### 🎥 Learn More (Deep Explanation in Hindi)")
    st.markdown("""
    - [🔗 WebSockets Tutorial in Hindi (CodeWithHarry)](https://www.youtube.com/watch?v=8ARodQ4Wlf4)  
    - [🔗 Real-Time Chat App with Node.js & WebSockets (Hindi)](https://www.youtube.com/watch?v=sj0p9O85AIg)  
    """)

elif chapter == "Chapter 11 Quiz":
    st.header("🧩 Chapter 11 Quiz: Real-Time Backend & WebSockets")

    score = 0

    q1 = st.radio("1. WebSockets allow communication that is:", 
                  ["One-way (client → server only)", 
                   "Two-way (client ↔ server)", 
                   "Only server to client"], index=None)
    if q1:
        if q1 == "Two-way (client ↔ server)":
            st.success("✅ Correct! WebSockets support two-way communication.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q2 = st.radio("2. Which protocol is WebSocket based on?", 
                  ["HTTP", "TCP", "UDP", "SMTP"], index=None)
    if q2:
        if q2 == "TCP":
            st.success("✅ Correct! WebSockets use TCP for persistent connections.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q3 = st.radio("3. What is a common use case of WebSockets?", 
                  ["Static website hosting", 
                   "Real-time chat", 
                   "Image compression", 
                   "Database backups"], index=None)
    if q3:
        if q3 == "Real-time chat":
            st.success("✅ Correct! WebSockets are widely used in chat apps.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q4 = st.radio("4. In Node.js, which package is commonly used for WebSockets?", 
                  ["express", "ws", "axios", "mongodb"], index=None)
    if q4:
        if q4 == "ws":
            st.success("✅ Correct! The `ws` package is a popular WebSocket library.")
            score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    if q1 and q2 and q3 and q4:  # show results only when all answered
        st.subheader(f"📊 Score: {score}/4")
        if score >= 3:
            st.session_state.xp += 10
            st.success("🏆 Great job! You earned +10 XP.")

            # 🔑 Mark Chapter 1 as completed
            st.session_state.completed_chapters.add(11)
            save_progress()
        else:
            st.warning("⚠️ Score less than 3. Try again to earn XP.")


elif chapter == "Chapter 11 Tasks":
    st.header("📝 Chapter 11 Tasks: Real-Time Backend & WebSockets")
    st.write("Practice building **real-time features** with WebSockets.")

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Create a simple WebSocket server in Node.js that:
       - Accepts connections  
       - Prints any message received from the client  
       - Replies with `"Message received"`  

    2. Build a **chat application**:
       - Multiple clients can connect  
       - Messages from one client are broadcast to all connected clients  

    3. Add a **real-time counter**:
       - Every time a new client connects, broadcast the total number of users online  

    4. Create a **notification system**:
       - When a client sends `"notify"`, all clients should receive `"🔔 New Notification!"`  

    5. (Bonus) Build a **real-time stock price simulator**:
       - Server randomly updates a stock price every 2 seconds  
       - All connected clients see the updated price instantly
    """)

elif chapter == "Chapter 12: Testing & Debugging":
    st.header("🐞 Chapter 12: Testing & Debugging Backend")
    chapter_divider(12)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    Debugging and testing are essential for reliable backend development.  

    **🔍 Debugging** → Finding and fixing errors in your code.  
    **🧪 Testing** → Writing code that checks if your backend works correctly.  

    Common Testing Types:  
    - ✅ **Unit Tests**: Test individual functions or modules.  
    - 🔗 **Integration Tests**: Test how different modules work together.  
    - 🌐 **API Tests**: Ensure endpoints return the expected data.  

    Popular Tools:  
    - **Jest / Mocha** → JavaScript testing frameworks.  
    - **Supertest** → For testing Express APIs.  
    - **Postman / Thunder Client** → Manual API testing.  

    Let's look at examples:
    """)

    st.subheader("📜 Example 1: Unit Test with Jest")
    st.code("""
    // math.js
    function add(a, b) {
        return a + b;
    }
    module.exports = add;

    // math.test.js
    const add = require('./math');

    test('adds 2 + 3 to equal 5', () => {
        expect(add(2, 3)).toBe(5);
    });
    """, language="javascript")

    st.subheader("📜 Example 2: API Test with Supertest")
    st.code("""
    const request = require('supertest');
    const app = require('./app'); // your Express app

    describe('GET /', () => {
      it('should return Hello World', async () => {
        const res = await request(app).get('/');
        expect(res.statusCode).toBe(200);
        expect(res.text).toBe('Hello World');
      });
    });
    """, language="javascript")

    st.success("With testing & debugging, your backend becomes **more reliable and professional**!")

    st.markdown("### 🎥 Learn More (Hindi Videos)")
    st.markdown("""
    - [🔗 Backend Testing with Jest (Hindi)](https://www.youtube.com/watch?v=MbJsvNYbMHo)  
    - [🔗 Postman API Testing Tutorial (Hindi)](https://www.youtube.com/watch?v=vyu2xWbJ0PQ)  
    """)

elif chapter == "Chapter 12 Quiz":
    st.header("🧩 Chapter 12 Quiz: Testing & Debugging")

    score = 0

    q1 = st.radio("1. What is the purpose of unit testing?", 
                  ["To test the whole application", 
                   "To test individual functions or modules", 
                   "To deploy applications"], index=None)
    if q1:
        if q1 == "To test individual functions or modules":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q2 = st.radio("2. Which tool is commonly used for API testing?", 
                  ["Excel", "Postman", "MongoDB", "React"], index=None)
    if q2:
        if q2 == "Postman":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q3 = st.radio("3. In Jest, which function is used to check results?", 
                  ["verify()", "check()", "expect()", "assert()"], index=None)
    if q3:
        if q3 == "expect()":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q4 = st.radio("4. What type of test checks how modules work together?", 
                  ["Unit Test", "Integration Test", "Security Test", "UI Test"], index=None)
    if q4:
        if q4 == "Integration Test":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    if q1 and q2 and q3 and q4:
        st.subheader(f"📊 Score: {score}/4")
        if score >= 3:
            st.session_state.xp += 10
            st.success("🏆 You earned +10 XP!")

            # 🔑 Mark Chapter 1 as completed
            st.session_state.completed_chapters.add(12)
            save_progress()
        else:
            st.warning("⚠️ Try again to earn XP.")


elif chapter == "Chapter 12 Tasks":
    st.header("📝 Chapter 12 Tasks: Testing & Debugging")

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Write a unit test in Jest for a function that multiplies two numbers.  

    2. Create an Express app with a route `/hello` that returns `"Hello Backend"`.  
       Write a Supertest case to check this response.  

    3. Write a unit test for a function that checks if a number is even.  

    4. Build an API with `/add?a=5&b=10` → returns the sum.  
       Write an API test to confirm correct output.  

    5. Intentionally add a bug in your code, run tests, and fix the error using debugging.
    """)

elif chapter == "Chapter 13: CI/CD & Automated Deployment":
    st.header("⚙️ Chapter 13: CI/CD & Automated Deployment")
    chapter_divider(13)
# 🔒 Lock check
    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()
    st.write("""
    CI/CD stands for **Continuous Integration and Continuous Deployment**.  
    It helps developers automatically test, build, and release their backend apps.  

    - **CI (Continuous Integration)** → Code is automatically tested every time a developer pushes changes.  
    - **CD (Continuous Deployment/Delivery)** → Code is automatically deployed to a server (like AWS, Heroku, Vercel).  

    Benefits:  
    - 🚀 Faster delivery  
    - ✅ Fewer bugs in production  
    - 🔄 Automated workflow  

    Popular CI/CD Tools:  
    - **GitHub Actions**  
    - **Jenkins**  
    - **GitLab CI**  
    - **CircleCI**  
    """)

    st.subheader("📜 Example: GitHub Actions Workflow")
    st.code("""
    # .github/workflows/node.js.yml
    name: Node.js CI

    on:
      push:
        branches: [ "main" ]
      pull_request:
        branches: [ "main" ]

    jobs:
      build:
        runs-on: ubuntu-latest

        steps:
        - name: Checkout code
          uses: actions/checkout@v2

        - name: Use Node.js
          uses: actions/setup-node@v2
          with:
            node-version: '16'

        - name: Install dependencies
          run: npm install

        - name: Run tests
          run: npm test
    """, language="yaml")

    st.success("With CI/CD, your backend is tested and deployed automatically whenever you push code!")

    st.markdown("### 🎥 Learn More (Hindi Videos)")
    st.markdown("""
    - [🔗 GitHub Actions CI/CD Tutorial (Hindi)](https://www.youtube.com/watch?v=fgbzTvF8ixs)  
    - [🔗 Jenkins CI/CD Pipeline (Hindi)](https://www.youtube.com/watch?v=f-Id9kYQKfw)  
    """)

elif chapter == "Chapter 13 Quiz":
    st.header("🧩 Chapter 13 Quiz: CI/CD & Automated Deployment")

    score = 0

    q1 = st.radio("1. What does CI in CI/CD stand for?", 
                  ["Continuous Integration", "Continuous Improvement", "Code Injection"], index=None)
    if q1:
        if q1 == "Continuous Integration":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q2 = st.radio("2. Which tool is commonly used for CI/CD?", 
                  ["GitHub Actions", "MongoDB", "React", "VS Code"], index=None)
    if q2:
        if q2 == "GitHub Actions":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q3 = st.radio("3. What does CD stand for?", 
                  ["Continuous Design", "Continuous Deployment", "Continuous Debugging"], index=None)
    if q3:
        if q3 == "Continuous Deployment":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q4 = st.radio("4. What is one key benefit of CI/CD?", 
                  ["Manual deployment", "Faster and automated delivery", "More bugs in production"], index=None)
    if q4:
        if q4 == "Faster and automated delivery":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    if q1 and q2 and q3 and q4:
        st.subheader(f"📊 Score: {score}/4")
        if score >= 3:
            st.session_state.xp += 10
            st.success("🏆 You earned +10 XP!")

            # 🔑 Mark Chapter 1 as completed
            st.session_state.completed_chapters.add(13)
            save_progress()
        else:
            st.warning("⚠️ Try again to earn XP.")


elif chapter == "Chapter 13 Tasks":
    st.header("📝 Chapter 13 Tasks: CI/CD & Automated Deployment")

    st.subheader("✅ Coding Tasks")
    st.markdown("""
    1. Create a simple Node.js app with a single API endpoint.  
    2. Write a test for the app using Jest.  
    3. Push your project to GitHub.  
    4. Add a `.github/workflows/node.js.yml` file to set up GitHub Actions.  
    5. Ensure your workflow runs automatically on every push to `main`.  
    6. Deploy your app to a platform (Heroku, Vercel, or Render).  
    7. Automate deployment in CI/CD so pushing new code redeploys your app.
    """)

# ---------------- Chapter 14: Authentication & Security ----------------
elif chapter == "Chapter 14: Authentication & Security":
    st.header("🔐 Chapter 14: Authentication & Security")
    chapter_divider(14)

    if st.session_state.xp < 20:
        st.warning("🔒 This chapter is locked! Earn 20 XP to unlock.")
        st.stop()

    st.write("""
    Security is **essential** for protecting user data and preventing unauthorized access.  

    ### 🔹 Authentication vs Authorization
    - **Authentication** → Verifying *who the user is* (e.g., login with username/password).  
    - **Authorization** → Verifying *what the user can do* (e.g., admin vs normal user).  

    ### 🔹 Common Authentication Methods
    - **Passwords** (basic, but must be stored securely with hashing like `bcrypt`).  
    - **OTP / Email Verification**.  
    - **OAuth2** (Login with Google, GitHub, Facebook).  
    - **JWT (JSON Web Tokens)** for API authentication.  

    ### 🔹 Security Best Practices
    - Hash + Salt passwords (never store plain text).  
    - Use HTTPS for secure communication.  
    - Apply **rate limiting** to stop brute-force attacks.  
    - Keep sensitive data in **environment variables**, not in code.  

    ### Example (Python: Password Hashing)
    ```python
    import bcrypt  

    # Hash password
    password = b"mypassword123"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    # Verify password
    if bcrypt.checkpw(password, hashed):
        print("✅ Password matches!")
    else:
        print("❌ Invalid password")
    ```
    """)

    st.success("✅ Authentication + Security keeps your app safe and trustworthy!")

    st.markdown("### 🎥 Learn More (Hindi Video)")
    st.link_button("📺 Authentication & Security Basics", "https://www.youtube.com/watch?v=7Q17ubqLfaM")


# ---------------- Chapter 14 Quiz ----------------
elif chapter == "Chapter 14 Quiz":
    st.header("🧩 Chapter 14 Quiz: Authentication & Security")

    score = 0  

    q1 = st.radio("1. What does Authentication mean?", 
                  ["Verifying who the user is", "Verifying what the user can do", "Encrypting data", "Storing passwords"], index=None)
    if q1:
        if q1 == "Verifying who the user is":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q2 = st.radio("2. Which of these is a secure way to store passwords?", 
                  ["Plain text", "MD5 only", "Hashing with bcrypt", "Storing in a text file"], index=None)
    if q2:
        if q2 == "Hashing with bcrypt":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q3 = st.radio("3. Which protocol ensures secure communication over the web?", 
                  ["HTTP", "FTP", "SMTP", "HTTPS"], index=None)
    if q3:
        if q3 == "HTTPS":
            st.success("✅ Correct!")
            score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Wrong!")

    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {score}/3")
        if score == 3:
            st.success("🌟 Excellent! You understand security basics.")
        elif score == 2:
            st.info("👍 Good job! Review once more to strengthen.")
        else:
            st.warning("💡 Needs improvement — keep practicing!")

        st.session_state.xp += 20

        # 🔑 Mark Chapter 1 as completed
        st.session_state.completed_chapters.add(14)
        save_progress()
        st.success("🏆 You earned +20 XP!")


# ---------------- Chapter 14 Tasks ----------------
elif chapter == "Chapter 14 Tasks":
    st.header("📝 Chapter 14 Tasks: Authentication & Security")
    st.markdown("""
    ✅ Hands-on Practice Challenges:  

    1. Implement a **login system** with username and password.  

    2. Use `bcrypt` in Python to **hash passwords** before storing them.  

    3. Add a feature → login fails after **3 wrong attempts**.  

    4. Implement a simple **JWT token-based authentication** for an API.  

    5. Bonus → Integrate **Google OAuth2 Login** using a library like `authlib`.  
    """)


# ---------------- Chapter 15: Databases & SQL ----------------
elif chapter == "Chapter 15: Databases & SQL":
    st.header("🗄️ Chapter 15: Databases & SQL")
    chapter_divider(15)

    if st.session_state.xp < 30:
        st.warning("🔒 This chapter is locked! Earn 30 XP to unlock.")
        st.stop()

    st.write("""
    Databases are used to **store, organize, and manage data** efficiently.  
    SQL (**Structured Query Language**) is the standard language to interact with databases.  

    ### 🔹 Types of Databases
    - **Relational (SQL)** → MySQL, PostgreSQL, SQLite (tables with rows & columns).  
    - **NoSQL** → MongoDB, Firebase (document-based, key-value, graph).  

    ### 🔹 Why Databases?
    - 📂 Store large amounts of data  
    - 🔍 Fast search & filtering  
    - 🔒 Secure and consistent  
    - 🤝 Multiple users can access simultaneously  

    ### 🔹 Common SQL Commands
    - `CREATE TABLE` → Make a new table  
    - `INSERT INTO` → Add new data  
    - `SELECT` → Retrieve data  
    - `UPDATE` → Modify existing data  
    - `DELETE` → Remove data  

    ### Example:
    ```sql
    CREATE TABLE Students (
        id INT PRIMARY KEY,
        name TEXT,
        age INT
    );

    INSERT INTO Students VALUES (1, 'Ali', 21);
    SELECT * FROM Students;
    ```
    """)

    st.success("✅ Databases are the backbone of almost every app — from small websites to enterprise systems!")

    st.markdown("### 🎥 Learn More (Hindi Video)")
    st.link_button("📺 SQL Database Tutorial", "https://www.youtube.com/watch?v=HXV3zeQKqGY")


# ---------------- Chapter 15 Quiz ----------------
elif chapter == "Chapter 15 Quiz":
    st.header("🧩 Chapter 15 Quiz: Databases & SQL")

    score = 0  

    q1 = st.radio("1. Which language is used to interact with relational databases?", 
                  ["Python", "C++", "SQL", "HTML"], index=None)
    if q1:
        if q1 == "SQL":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q2 = st.radio("2. Which SQL command is used to retrieve data?", 
                  ["INSERT", "SELECT", "DELETE", "UPDATE"], index=None)
    if q2:
        if q2 == "SELECT":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q3 = st.radio("3. Which of these is a NoSQL database?", 
                  ["PostgreSQL", "MySQL", "MongoDB", "SQLite"], index=None)
    if q3:
        if q3 == "MongoDB":
            st.success("✅ Correct!")
            score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Wrong!")

    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {score}/3")
        if score == 3:
            st.success("🌟 Excellent! You mastered SQL basics.")
        elif score == 2:
            st.info("👍 Good job! A little revision will help.")
        else:
            st.warning("💡 Keep practicing, you’ll get there!")

        st.session_state.xp += 20
                # 🔑 Mark Chapter 1 as completed
        st.session_state.completed_chapters.add(15)
        st.success("🏆 You earned +20 XP!")
        save_progress()


# ---------------- Chapter 15 Tasks ----------------
elif chapter == "Chapter 15 Tasks":
    st.header("📝 Chapter 15 Tasks: Databases & SQL")
    st.markdown("""
    ✅ Hands-on Practice Challenges:  

    1. Install SQLite (or use an online SQL editor).  

    2. Create a **Students** table with columns: `id`, `name`, `age`.  

    3. Insert at least **5 students** into the table.  

    4. Write a query to **fetch all students older than 20 years**.  

    5. Update one student’s name and delete another student’s record.  

    6. Bonus → Try creating a second table (e.g., Courses) and use a **JOIN** query.  
    """)

# ---------------- Chapter 16: Containerization with Docker ----------------
elif chapter == "Chapter 16: Containerization with Docker":
    st.header("🐳 Chapter 16: Containerization with Docker")
    chapter_divider(16)

    if st.session_state.xp < 50:
        st.warning("🔒 This chapter is locked! Earn 50 XP to unlock.")
        st.stop()

    st.write("""
    Docker allows developers to **package applications** and all their dependencies into **containers**,  
    making them portable, consistent, and easy to run anywhere.  

    ### 🔹 Why Docker?
    - 🏗️ **Consistency** → Same environment everywhere (no "works on my machine" issues).  
    - ⚡ **Lightweight** → Uses fewer resources than Virtual Machines.  
    - 🚀 **Scalability** → Easy to run multiple containers.  
    - 🔄 **Portability** → Works across Windows, Linux, Mac, and cloud.  

    ### 🔹 Key Concepts:
    - **Image** → Blueprint of your application.  
    - **Container** → Running instance of an image.  
    - **Dockerfile** → Script with instructions to build images.  
    - **Docker Hub** → Public registry to share images.  

    ### 🔹 Docker vs Virtual Machine
    - VM → Heavy (needs OS for each instance).  
    - Docker → Lightweight (shares host OS, only adds what’s needed).  
    """)

    st.subheader("🖥️ Example: Dockerfile for Node.js App")
    st.code("""
    # Dockerfile
    FROM node:16
    WORKDIR /app
    COPY package*.json ./
    RUN npm install
    COPY . .
    EXPOSE 3000
    CMD ["node", "server.js"]
    """, language="dockerfile")

    st.success("✅ With Docker, you can run your app anywhere — local, server, or cloud!")

    st.markdown("### 🎥 Learn More (Hindi Video)")
    st.link_button("📺 Docker Tutorial in Hindi", "https://www.youtube.com/watch?v=ns9tmyuF65k")


# ---------------- Chapter 16 Quiz ----------------
elif chapter == "Chapter 16 Quiz":
    st.header("🧩 Chapter 16 Quiz: Containerization with Docker")

    score = 0  

    q1 = st.radio("1. What does Docker package an app into?", 
                  ["Virtual Machine", "Container", "Library", "Script"], index=None)
    if q1:
        if q1 == "Container":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q2 = st.radio("2. What is a Dockerfile used for?", 
                  ["To run containers", "To build Docker images", "To store passwords", "To install Node.js"], index=None)
    if q2:
        if q2 == "To build Docker images":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q3 = st.radio("3. Which is lighter: Docker containers or Virtual Machines?", 
                  ["Containers", "Virtual Machines", "Both same", "None"], index=None)
    if q3:
        if q3 == "Containers":
            st.success("✅ Correct!")
            score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Wrong!")

    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {score}/3")
        if score == 3:
            st.success("🌟 Excellent! You mastered Docker basics.")
        elif score == 2:
            st.info("👍 Good job! A little revision will help.")
        else:
            st.warning("💡 Keep practicing, you’ll get there!")

        st.session_state.xp += 20
                # 🔑 Mark Chapter 1 as completed
        st.session_state.completed_chapters.add(16)
        st.success("🏆 You earned +20 XP!")
        save_progress()


# ---------------- Chapter 16 Tasks ----------------
elif chapter == "Chapter 16 Tasks":
    st.header("📝 Chapter 16 Tasks: Containerization with Docker")
    st.markdown("""
    ✅ Hands-on Practice Challenges:  

    1. Install Docker and run the command:  
       ```bash
       docker run hello-world
       ```
       to verify installation.  

    2. Create a **Dockerfile** for a Node.js app and build the image.  

    3. Run your app inside a container and test in the browser.  

    4. Push your Docker image to **Docker Hub**.  

    5. Compare the performance of running an app **with Docker** vs **without Docker**.  
    """)


# ---------------- Chapter 17: Kubernetes & Orchestration ----------------
elif chapter == "Chapter 17: Kubernetes & Orchestration":
    st.header("☸️ Chapter 17: Kubernetes & Orchestration")
    chapter_divider(17)

    if st.session_state.xp < 100:
        st.warning("🔒 This chapter is locked! Earn 100 XP to unlock.")
        st.stop()

    st.write("""
    Kubernetes (often called **K8s**) is a powerful system for **orchestrating containers**.  
    Imagine you have multiple Docker containers (your app, database, cache, etc.) —  
    Kubernetes helps you manage them all **automatically**.  

    ### 🔹 Why Kubernetes?
    - 🚀 **Scalability** → Automatically increase or decrease containers depending on traffic.  
    - ⚡ **Self-Healing** → If a container crashes, Kubernetes restarts it.  
    - 🌍 **Load Balancing** → Distributes traffic across containers evenly.  
    - 🔄 **Rolling Updates** → Update your app without downtime.  

    ### 🔹 Key Concepts in Kubernetes:
    - **Cluster** → A group of machines (nodes) where Kubernetes runs.  
    - **Node** → A single machine (VM/Server) inside the cluster.  
    - **Pod** → The smallest unit in Kubernetes (can contain one or more containers).  
    - **Deployment** → Ensures the right number of Pods are running at all times.  
    - **Service** → Exposes Pods so users or other apps can access them.  
    - **Ingress** → Manages external traffic (like a gateway + load balancer).  

    ### 🔹 Workflow
    1. Developer writes a **Dockerfile** → builds an image.  
    2. Push image to **Docker Hub** (or any registry).  
    3. Create a **Kubernetes Deployment** (YAML file).  
    4. Apply it with `kubectl apply -f deployment.yaml`.  
    5. Kubernetes schedules pods, ensures scaling, and keeps everything running.  
    """)

    st.subheader("🖥️ Example: Kubernetes Deployment (YAML)")
    st.code("""
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: node-app
    spec:
      replicas: 3        # Run 3 copies of the app
      selector:
        matchLabels:
          app: node
      template:
        metadata:
          labels:
            app: node
        spec:
          containers:
          - name: node
            image: my-node-app:1.0
            ports:
            - containerPort: 3000
    """, language="yaml")

    st.success("✅ Kubernetes makes apps **scalable, resilient, and production-ready**!")

    # 🎥 YouTube Video Section
    st.markdown("### 🎥 Learn More with Video Tutorials (Hindi)")
    col1, col2 = st.columns(2)

    with col1:
        st.link_button("📺 Kubernetes in Hindi (Complete Guide)", 
                       "https://www.youtube.com/watch?v=Jt0zVxgkGcQ")

    with col2:
        st.link_button("📺 Kubernetes Deployment Tutorial", 
                       "https://www.youtube.com/watch?v=VnvRFRk_51k")

# ---------------- Chapter 17 Quiz ----------------
elif chapter == "Chapter 17 Quiz":
    st.header("🧩 Chapter 17 Quiz: Kubernetes & Orchestration")

    score = 0  

    q1 = st.radio("1. What is the smallest unit in Kubernetes?", 
                  ["Pod", "Deployment", "Service"], index=None)
    if q1 == "Pod":
        st.success("✅ Correct!")
        score += 1
    elif q1:
        st.error("❌ Try again!")

    q2 = st.radio("2. Which object ensures the desired number of pods?", 
                  ["Ingress", "Deployment", "ReplicaSet"], index=None)
    if q2 == "Deployment":
        st.success("✅ Correct!")
        score +=1 
        save_progress()

    elif q2:
        st.error("❌ Try again!")

    q3 = st.radio("3. Which component exposes pods to the network?", 
                  ["Service", "ConfigMap", "Pod"], index=None)
    if q3 == "Service":
        st.success("✅ Correct!")
        score += 1
        save_progress()
    elif q3:
        st.error("❌ Try again!")

    # Show score and XP
    st.markdown(f"### 🏆 Your Score: {score}/3")

    if score == 3:
        st.session_state.xp += 10
        st.success("🎉 Perfect! You earned **10 XP**")
    elif score == 2:
        st.session_state.xp += 5
        st.info("👍 Good job! You earned **5 XP**")

                # 🔑 Mark Chapter 1 as completed
        st.session_state.completed_chapters.add(17)
        save_progress()
    else:
        st.warning("⚡ Keep trying to score better and earn XP!")


# ---------------- Chapter 17 Tasks ----------------
elif chapter == "Chapter 17 Tasks":
    st.header("📝 Chapter 17 Tasks: Kubernetes & Orchestration")
    st.subheader("✅ Practical Tasks")
    st.markdown("""
    1. Install Minikube or use a Kubernetes cluster.  
    2. Deploy a Node.js app using a Deployment YAML file.  
    3. Expose it using a Service of type NodePort.  
    4. Scale your deployment from 2 pods to 5 pods.  
    5. Add an Ingress rule to route traffic to your service.  
    """)

# ---------------- Chapter 18: Cloud Deployment ----------------
elif chapter == "Chapter 18: Cloud Deployment (AWS/GCP/Azure)":
    st.header("☁️ Chapter 18: Cloud Deployment (AWS/GCP/Azure)")
    chapter_divider(18)

    if st.session_state.xp < 150:
        st.warning("🔒 This chapter is locked! Earn 150 XP to unlock.")
        st.stop()

    st.write("""
    Cloud platforms allow developers to **deploy apps globally** without setting up their own hardware.  
    Instead of buying and maintaining servers, you can **rent computing power** from cloud providers.

    ### 🔹 Why Cloud?
    - 🌍 Deploy apps for worldwide access.  
    - ⚡ Auto-scale when traffic increases.  
    - 💰 Pay only for what you use.  
    - 🔒 Secure & reliable infrastructure.  

    ### 🔹 Popular Providers:
    - **AWS (Amazon Web Services)** → EC2, S3, Lambda, ECS, RDS  
    - **GCP (Google Cloud Platform)** → Compute Engine, GKE, Cloud Functions  
    - **Azure (Microsoft)** → Azure VM, AKS, Azure Functions  

    ### 🔹 Deployment Options:
    1. **Virtual Machines (IaaS)**  
       - Example: AWS EC2, GCP Compute Engine  
       - Gives you full control (like renting a server).  

    2. **Containers (CaaS)**  
       - Example: AWS ECS, GCP GKE, Azure AKS  
       - Run Docker/Kubernetes apps easily.  

    3. **Serverless (FaaS)**  
       - Example: AWS Lambda, GCP Cloud Functions  
       - No servers to manage → just upload your code!  

    👉 Cloud = Flexibility, Scalability, and Global Reach 🚀
    """)

    st.markdown("### 🎥 Learn More (Hindi Video)")
    st.link_button("📺 Cloud Computing Basics in Hindi", "https://www.youtube.com/watch?v=2LaAJq1lB1Q")


# ---------------- Chapter 18 Quiz ----------------
elif chapter == "Chapter 18 Quiz":
    st.header("🧩 Chapter 18 Quiz: Cloud Deployment")

    st.session_state.score = 0
    st.session_state.total_questions = 3

    q1 = st.radio("1. Which of these is NOT a cloud provider?", 
                  ["AWS", "GCP", "Azure", "Photoshop"], index=None)
    if q1:
        if q1 == "Photoshop":
            st.success("✅ Correct!")
            st.session_state.score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q2 = st.radio("2. What does 'Serverless' mean?", 
                  ["No servers exist", "Cloud manages servers for you", "Only frontend apps"], index=None)
    if q2:
        if q2 == "Cloud manages servers for you":
            st.success("✅ Correct!")
            st.session_state.score += 1
            save_progress()
        else:
            st.error("❌ Try again!")

    q3 = st.radio("3. Which service is 'Infrastructure as a Service (IaaS)'?", 
                  ["AWS EC2", "AWS Lambda", "Firebase", "Google Docs"], index=None)
    if q3:
        if q3 == "AWS EC2":
            st.success("✅ Correct!")
            st.session_state.score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Nope!")

    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {st.session_state.score}/3")
        if st.session_state.score == 3:
            st.success("🌟 Excellent! You mastered Cloud basics.")
        elif st.session_state.score == 2:
            st.info("👍 Good job! Review once more for clarity.")
        else:
            st.warning("💡 Keep practicing.")
        st.session_state.xp += 15
        st.session_state.completed_chapters.add(18)
        st.success("🏆 You earned +15 XP!")
        save_progress()


# ---------------- Chapter 18 Tasks ----------------
elif chapter == "Chapter 18 Tasks":
    st.header("📝 Chapter 18 Tasks: Cloud Deployment")
    st.markdown("""
    ✅ Practice Challenges:  

    1. Deploy a simple Node.js or Python app on **Heroku or Render** (free tier).  
    2. Try AWS Free Tier → Launch an EC2 instance and install Node.js.  
    3. Deploy a Docker container on **Google Kubernetes Engine (GKE)**.  
    4. Create a serverless function in AWS Lambda that returns `"Hello Cloud"`.  
    5. Compare pricing between **AWS, GCP, and Azure** for hosting a small app.  
    """)
# ---------------- Chapter 19: CI/CD Pipelines ----------------
elif chapter == "Chapter 19: CI/CD Pipelines":
    st.header("⚙️ Chapter 19: CI/CD Pipelines")
    chapter_divider(19)

    if st.session_state.xp < 200:
        st.warning("🔒 This chapter is locked! Earn 200 XP to unlock.")
        st.stop()

    st.write("""
    CI/CD stands for **Continuous Integration** and **Continuous Deployment/Delivery**.  
    It helps developers **automate testing, building, and deployment** → making development faster and safer.  

    ### 🔹 CI (Continuous Integration)
    - Developers push code frequently (daily or multiple times a day).  
    - Each push triggers automated tests & build pipeline.  
    - Ensures **new code doesn’t break existing code**.  

    ### 🔹 CD (Continuous Deployment/Delivery)
    - **Continuous Delivery** → Code is automatically tested and ready for manual deployment.  
    - **Continuous Deployment** → Code is automatically deployed to servers after passing all tests.  

    ### 🔹 Benefits of CI/CD
    - 🚀 Faster releases  
    - ✅ Fewer bugs in production  
    - 🔁 Automated testing saves time  
    - ⚡ Scalable development for teams  

    ### 🔹 Popular CI/CD Tools:
    - **GitHub Actions**  
    - **GitLab CI/CD**  
    - **Jenkins**  
    - **CircleCI**  
    """)

    st.markdown("### 🎥 Learn More (Hindi Video)")
    st.link_button("📺 CI/CD Explained in Hindi", "https://www.youtube.com/watch?v=R8_veQiYBjI")


# ---------------- Chapter 19 Quiz ----------------
elif chapter == "Chapter 19 Quiz":
    st.header("🧩 Chapter 19 Quiz: CI/CD Pipelines")

    st.session_state.score = 0
    st.session_state.total_questions = 3

    q1 = st.radio("1. What does CI stand for?", 
                  ["Continuous Integration", "Cloud Infrastructure", "Centralized Information"], index=None)
    if q1:
        if q1 == "Continuous Integration":
            st.success("✅ Correct!")
            st.session_state.score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q2 = st.radio("2. Which tool is commonly used for CI/CD?", 
                  ["GitHub Actions", "MS Word", "Excel", "Figma"], index=None)
    if q2:
        if q2 == "GitHub Actions":
            st.success("✅ Correct!")
            st.session_state.score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q3 = st.radio("3. What is the main advantage of CI/CD?", 
                  ["Slower releases", "Fewer bugs & faster deployment", "No testing needed"], index=None)
    if q3:
        if q3 == "Fewer bugs & faster deployment":
            st.success("✅ Correct!")
            st.session_state.score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Wrong!")

    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {st.session_state.score}/3")
        if st.session_state.score == 3:
            st.success("🌟 Excellent! You mastered CI/CD basics.")
        elif st.session_state.score == 2:
            st.info("👍 Good effort! Review once more for clarity.")
        else:
            st.warning("💡 Keep practicing.")
        st.session_state.xp += 15
        # 🔑 Mark Chapter 1 as completed
        st.session_state.completed_chapters.add(19)
        st.success("🏆 You earned +15 XP!")
        save_progress()


# ---------------- Chapter 19 Tasks ----------------
elif chapter == "Chapter 19 Tasks":
    st.header("📝 Chapter 19 Tasks: CI/CD Pipelines")
    st.markdown("""
    ✅ Practice Challenges:  

    1. Create a **GitHub Actions** workflow that runs tests when you push code.  
    2. Use **GitLab CI/CD** to automatically deploy a small app to Heroku.  
    3. Write a **Jenkins pipeline** that builds and tests your project.  
    4. Automate deployment of a Node.js or Python app after every commit.  
    5. Research → Compare GitHub Actions vs Jenkins (advantages & disadvantages).  
    """)


# ---------------- Chapter 20: WebSockets ----------------
elif chapter == "Chapter 20: WebSockets":
    st.header("🔌 Chapter 20: WebSockets & Real-time Communication")
    chapter_divider(20)

    if st.session_state.xp < 250:
        st.warning("🔒 This chapter is locked! Earn 250 XP to unlock.")
        st.stop()

    st.write("""
    WebSockets enable **real-time two-way communication** between client and server.  
    Unlike HTTP (request-response model), WebSockets keep a **persistent connection open**.  

    ### 🔹 Why WebSockets?
    - 📡 Real-time communication without constant HTTP requests.  
    - ⚡ Faster & more efficient for frequent updates.  
    - 🎮 Ideal for **chats, games, notifications, live dashboards**.  

    ### 🔹 How WebSockets Work
    1. Client sends a request to **upgrade** HTTP → WebSocket.  
    2. Server accepts, and connection stays **open**.  
    3. Both client & server can now **send/receive anytime**.  

    ### 🔹 Common Use Cases
    - 💬 **Chat apps**  
    - 🎮 **Multiplayer games**  
    - 📊 **Live dashboards (stocks, crypto, analytics)**  
    - 🔔 **Push notifications**  
    """)

    st.subheader("🖥️ Example: WebSocket Server (Node.js)")
    st.code("""
    const WebSocket = require('ws');
    const server = new WebSocket.Server({ port: 8080 });

    server.on('connection', socket => {
        console.log('Client connected');
        socket.send('Welcome to WebSocket server!');

        socket.on('message', msg => {
            console.log('Message:', msg);
            socket.send(`Echo: ${msg}`);
        });
    });
    """, language="javascript")

    st.success("✅ With WebSockets, your backend can handle **real-time data** easily!")

    st.markdown("### 🎥 Learn More (Hindi Video)")
    st.link_button("📺 WebSockets in Hindi", "https://www.youtube.com/watch?v=2Nt-ZrNP22A")


# ---------------- Chapter 20 Quiz ----------------
elif chapter == "Chapter 20 Quiz":
    st.header("🧩 Chapter 20 Quiz: WebSockets")

    if "score" not in st.session_state:
        st.session_state.score = 0

    score = 0  

    q1 = st.radio("1. What makes WebSockets different from HTTP?", 
                  ["One-way request/response only", 
                   "Two-way persistent communication", 
                   "Slower than HTTP"], index=None)
    if q1:
        if q1 == "Two-way persistent communication":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q2 = st.radio("2. Which is NOT a common use case of WebSockets?", 
                  ["Chat apps", "Live dashboards", "Static websites", "Notifications"], index=None)
    if q2:
        if q2 == "Static websites":
            st.success("✅ Correct!")
            score += 1
            save_progress()
        else:
            st.error("❌ Wrong!")

    q3 = st.radio("3. Which Node.js library is often used for WebSockets?", 
                  ["Express", "WebSocket (ws)", "MongoDB", "Postman"], index=None)
    if q3:
        if q3 == "WebSocket (ws)":
            st.success("✅ Correct!")
            score += 1
            save_progress()
            st.balloons()
        else:
            st.error("❌ Wrong!")

    if q1 and q2 and q3:
        st.subheader(f"📊 Score: {score}/3")
        if score == 3:
            st.success("🌟 Excellent! You mastered WebSockets.")
        elif score == 2:
            st.info("👍 Good job! Review once more.")
        else:
            st.warning("💡 Keep practicing, you’ll get there!")

        st.session_state.xp += 20
        # 🔑 Mark Chapter 1 as completed
        st.session_state.completed_chapters.add(20)
        st.success("🏆 You earned +20 XP!")
        save_progress()


# ---------------- Chapter 20 Tasks ----------------
elif chapter == "Chapter 20 Tasks":
    st.header("📝 Chapter 20 Tasks: WebSockets")
    st.markdown("""
    ✅ Hands-on Practice Challenges:  

    1. Create a **Node.js WebSocket server** that echoes client messages.  

    2. Build a **chat app** where multiple clients can talk in real-time.  

    3. Make a **live counter** → track and show number of online users.  

    4. Create a **real-time stock price dashboard** (simulate values updating every second).  

    5. Compare **WebSockets vs REST APIs** in terms of speed & efficiency.  
    """)

elif chapter == "Coding Games":


    st.title("🎮 Coding Games Dashboard")
    st.write("""
    Sharpen your backend skills while having fun!  
    Complete these mini-games to earn XP and unlock badges.
    """)

    # Initialize XP and badges
    if "game_xp" not in st.session_state:
        st.session_state.game_xp = 0

    if "badges" not in st.session_state:
        st.session_state.badges = []

    st.markdown("---")
    st.subheader(f"🏆 Total Game XP: {st.session_state.game_xp}")

    # ---------------- Game 1: Guess the Number ----------------
    st.subheader("1️⃣ Guess the Number (5 XP)")
    if "guess_number" not in st.session_state:
        st.session_state.guess_number = random.randint(1, 10)

    guess = st.number_input("Enter your guess (1-10):", min_value=1, max_value=10, step=1, key="guess_input")
    if st.button("Check Guess"):
        if guess == st.session_state.guess_number:
            st.success("🎉 Correct! +5 XP")
            st.session_state.game_xp += 5
            st.session_state.guess_number = random.randint(1, 10)
        else:
            st.warning("❌ Wrong! Try again.")

    st.markdown("---")

    # ---------------- Game 2: Quick Math Challenge ----------------
    st.subheader("2️⃣ Quick Math Challenge (5 XP)")
    if "num1" not in st.session_state:
        st.session_state.num1 = random.randint(1, 20)
        st.session_state.num2 = random.randint(1, 20)

    answer = st.number_input(f"What is {st.session_state.num1} + {st.session_state.num2}?", key="math_input")
    if st.button("Check Answer", key="math_btn"):
        if answer == st.session_state.num1 + st.session_state.num2:
            st.success("✅ Correct! +5 XP")
            st.session_state.game_xp += 5
            st.session_state.num1 = random.randint(1, 20)
            st.session_state.num2 = random.randint(1, 20)
        else:
            st.warning("❌ Wrong! Try again.")

    st.markdown("---")

    # ---------------- Game 3: String Reversal ----------------
    st.subheader("3️⃣ String Reversal Challenge (5 XP)")
    sample_string = "Backend"
    user_input = st.text_input(f"Reverse this string: {sample_string}", key="reverse_input")
    if st.button("Check Reverse"):
        if user_input == sample_string[::-1]:
            st.success("🎉 Correct! +5 XP")
            st.session_state.game_xp += 5
        else:
            st.warning("❌ Incorrect, try again.")

    st.markdown("---")

    # ---------------- Game 4: Memory Number Challenge ----------------
    st.subheader("4️⃣ Memory Number Challenge (10 XP)")
    if "memory_seq" not in st.session_state:
        st.session_state.memory_seq = [random.randint(1, 9) for _ in range(5)]

    st.write("💡 Memorize this sequence:", st.session_state.memory_seq)
    user_mem_input = st.text_input("Enter the sequence separated by commas:", key="memory_input")
    if st.button("Check Sequence"):
        try:
            user_seq = [int(x.strip()) for x in user_mem_input.split(",")]
            if user_seq == st.session_state.memory_seq:
                st.success("🎉 Perfect! +10 XP")
                st.session_state.game_xp += 10
                st.session_state.memory_seq = [random.randint(1, 9) for _ in range(5)]
            else:
                st.warning("❌ Wrong sequence! Try again.")
        except:
            st.error("⚠️ Enter numbers separated by commas!")

    st.markdown("---")

    # ---------------- Game 5: FizzBuzz Challenge ----------------
    st.subheader("5️⃣ FizzBuzz Challenge (10 XP)")
    user_fizzbuzz = st.text_area("Enter numbers 1-15, replacing multiples of 3 with 'Fizz', 5 with 'Buzz', 3&5 with 'FizzBuzz', separated by commas:", key="fizzbuzz_input")
    if st.button("Check FizzBuzz"):
        correct = []
        for i in range(1, 16):
            if i % 3 == 0 and i % 5 == 0:
                correct.append("FizzBuzz")
            elif i % 3 == 0:
                correct.append("Fizz")
            elif i % 5 == 0:
                correct.append("Buzz")
            else:
                correct.append(str(i))
        if user_fizzbuzz.split(",") == correct:
            st.success("🎉 Correct! +10 XP")
            st.session_state.game_xp += 10
        else:
            st.warning("❌ Not quite right, check multiples of 3 and 5.")

    st.markdown("---")

    # ---------------- Game 6: Mini Backend Quiz ----------------
    st.subheader("6️⃣ Mini Backend Quiz (5 XP per correct answer)")
    questions = {
        "What HTTP status code means 'Not Found'?": "404",
        "Which database is NoSQL?": "MongoDB",
        "Which HTTP method is used to delete a resource?": "DELETE"
    }

    for q, ans in questions.items():
        user_ans = st.text_input(q, key=f"quiz_{q}")
        if st.button(f"Check Answer for '{q}'"):
            if user_ans.strip().upper() == ans.upper():
                st.success("✅ Correct! +5 XP")
                st.session_state.game_xp += 5
            else:
                st.error(f"❌ Wrong! Correct answer: {ans}")

    st.markdown("---")

    # ---------------- Badges ----------------
    st.subheader("🏅 Badges Earned")
    if st.session_state.game_xp >= 50 and "Game Master" not in st.session_state.badges:
        st.session_state.badges.append("Game Master")
    if st.session_state.game_xp >= 25 and "Backend Challenger" not in st.session_state.badges:
        st.session_state.badges.append("Backend Challenger")

    if st.session_state.badges:
        st.write("You have earned these badges:", ", ".join(st.session_state.badges))
    else:
        st.write("No badges yet. Keep playing!")



