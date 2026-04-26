"""
Seed the database with 20 users, 35 skills, reviews, and booking requests.
Fully idempotent — safe to run multiple times; won't create duplicates.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from marketplace.models import BookingRequest, Review, Skill

User = get_user_model()

# ── 20 Users ───────────────────────────────────────────────────────────────────

USERS = [
    {"username": "alice",   "email": "alice@baylor.edu",   "password": "skillswap2024", "first_name": "Alice",   "last_name": "Nguyen"},
    {"username": "bob",     "email": "bob@baylor.edu",     "password": "skillswap2024", "first_name": "Bob",     "last_name": "Martinez"},
    {"username": "carol",   "email": "carol@baylor.edu",   "password": "skillswap2024", "first_name": "Carol",   "last_name": "Chen"},
    {"username": "david",   "email": "david@baylor.edu",   "password": "skillswap2024", "first_name": "David",   "last_name": "Okonkwo"},
    {"username": "eve",     "email": "eve@baylor.edu",     "password": "skillswap2024", "first_name": "Eve",     "last_name": "Patel"},
    {"username": "frank",   "email": "frank@baylor.edu",   "password": "skillswap2024", "first_name": "Frank",   "last_name": "Delgado"},
    {"username": "grace",   "email": "grace@baylor.edu",   "password": "skillswap2024", "first_name": "Grace",   "last_name": "Kim"},
    {"username": "henry",   "email": "henry@baylor.edu",   "password": "skillswap2024", "first_name": "Henry",   "last_name": "Brooks"},
    {"username": "iris",    "email": "iris@baylor.edu",    "password": "skillswap2024", "first_name": "Iris",    "last_name": "Nakamura"},
    {"username": "james",   "email": "james@baylor.edu",   "password": "skillswap2024", "first_name": "James",   "last_name": "Owusu"},
    {"username": "kate",    "email": "kate@baylor.edu",    "password": "skillswap2024", "first_name": "Kate",    "last_name": "Sullivan"},
    {"username": "liam",    "email": "liam@baylor.edu",    "password": "skillswap2024", "first_name": "Liam",    "last_name": "Torres"},
    {"username": "maya",    "email": "maya@baylor.edu",    "password": "skillswap2024", "first_name": "Maya",    "last_name": "Robinson"},
    {"username": "noah",    "email": "noah@baylor.edu",    "password": "skillswap2024", "first_name": "Noah",    "last_name": "Fischer"},
    {"username": "olivia",  "email": "olivia@baylor.edu",  "password": "skillswap2024", "first_name": "Olivia",  "last_name": "Reyes"},
    {"username": "peter",   "email": "peter@baylor.edu",   "password": "skillswap2024", "first_name": "Peter",   "last_name": "Andersen"},
    {"username": "quinn",   "email": "quinn@baylor.edu",   "password": "skillswap2024", "first_name": "Quinn",   "last_name": "Washington"},
    {"username": "rachel",  "email": "rachel@baylor.edu",  "password": "skillswap2024", "first_name": "Rachel",  "last_name": "Hoffman"},
    {"username": "sam",     "email": "sam@baylor.edu",     "password": "skillswap2024", "first_name": "Sam",     "last_name": "Adeyemi"},
    {"username": "tara",    "email": "tara@baylor.edu",    "password": "skillswap2024", "first_name": "Tara",    "last_name": "Lindqvist"},
]

# ── 35 Skills across all 4 categories ─────────────────────────────────────────

SKILLS = [

    # ── ACADEMIC (10) ──────────────────────────────────────────────────────────

    {
        "owner": "alice", "category": "Academic",
        "title": "Calculus I & II Tutoring",
        "description": (
            "Struggling with limits, derivatives, or integrals? I'm a junior Math major with two years "
            "of tutoring experience. We'll work through your homework and build real intuition — not just "
            "formulas. Flexible schedule, on or off campus. Great for MATH 1321/1322 students."
        ),
        "price": 15.00, "is_free": False, "contact_preference": "email",
        "contact_info": "alice@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "eve", "category": "Academic",
        "title": "Spanish Conversation Practice",
        "description": (
            "Native Spanish speaker from San Antonio. Let's practice conversation, correct your "
            "pronunciation, and prep for exams. Great for SPAN 1301/1302 students. Sessions are "
            "casual and fun — think coffee chat in Spanish. Beginners very welcome."
        ),
        "price": None, "is_free": True, "contact_preference": "chat",
        "contact_info": "eve_patel on iMessage", "availability_status": "available",
    },
    {
        "owner": "alice", "category": "Academic",
        "title": "Essay & Research Paper Coaching",
        "description": (
            "English minor here. I help with thesis statements, argument structure, citations "
            "(MLA/APA/Chicago), and overall flow. Whether it's a 2-page response or a 15-page "
            "research paper, I'll give you honest, constructive feedback. Turnaround in 48 hrs."
        ),
        "price": 10.00, "is_free": False, "contact_preference": "email",
        "contact_info": "alice@baylor.edu", "availability_status": "busy",
    },
    {
        "owner": "grace", "category": "Academic",
        "title": "Biology & Anatomy Tutoring",
        "description": (
            "Pre-med sophomore who aced BIO 1305 and 1306. I can help with cell biology, genetics, "
            "anatomy, and physiology. I use diagrams and mnemonics to make concepts stick. "
            "Perfect for students in pre-health tracks or intro biology courses."
        ),
        "price": 12.00, "is_free": False, "contact_preference": "in_person",
        "contact_info": "Baylor Science Building study rooms — DM to schedule",
        "availability_status": "available",
    },
    {
        "owner": "kate", "category": "Academic",
        "title": "General Chemistry Help",
        "description": (
            "Chemistry TA with three semesters of experience. I cover stoichiometry, thermodynamics, "
            "equilibrium, acids/bases, and electrochemistry. Bring your problem sets and we'll "
            "tackle them together. I can also help you prep for the ACS exam."
        ),
        "price": 14.00, "is_free": False, "contact_preference": "email",
        "contact_info": "kate@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "rachel", "category": "Academic",
        "title": "Psychology & Research Methods Tutoring",
        "description": (
            "PSY major with a minor in Statistics. I tutor intro psych, abnormal psych, "
            "and research methods including SPSS basics. I also help with APA-format papers "
            "and understanding study designs. Great for PSY 1305 or upper-level courses."
        ),
        "price": None, "is_free": True, "contact_preference": "email",
        "contact_info": "rachel@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "sam", "category": "Academic",
        "title": "Finance & Accounting Tutoring",
        "description": (
            "Finance major with a 4.0 in all BBA core courses. I help with financial statements, "
            "ratio analysis, time value of money, and managerial accounting. Also comfortable "
            "with Excel models for valuations. Great for ACC 2303/2304 and FIN 3310 students."
        ),
        "price": 18.00, "is_free": False, "contact_preference": "email",
        "contact_info": "sam@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "olivia", "category": "Academic",
        "title": "Creative Writing & Poetry Workshop",
        "description": (
            "English and Journalism double major. I host one-on-one writing sessions where we "
            "workshop your fiction, personal essays, or poetry. I focus on voice, structure, "
            "and revision — not just grammar. Published in two campus literary journals."
        ),
        "price": None, "is_free": True, "contact_preference": "chat",
        "contact_info": "olivia.reyes on Discord", "availability_status": "available",
    },
    {
        "owner": "eve", "category": "Academic",
        "title": "MCAT Verbal Reasoning Prep",
        "description": (
            "Pre-med senior with MCAT score of 515. I specialize in CARS strategy — "
            "active reading, passage mapping, and process of elimination. We'll do timed "
            "practice and full passage reviews. Available weekday evenings and Sunday afternoons."
        ),
        "price": 20.00, "is_free": False, "contact_preference": "email",
        "contact_info": "eve@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "grace", "category": "Academic",
        "title": "Statistics & Data Interpretation Help",
        "description": (
            "I help with descriptive stats, probability, hypothesis testing, regression, "
            "and interpreting SPSS/R output. Whether it's for a research methods class or "
            "a thesis, I break it down step by step. No prior stats background needed."
        ),
        "price": 13.00, "is_free": False, "contact_preference": "email",
        "contact_info": "grace@baylor.edu", "availability_status": "available",
    },

    # ── CREATIVE (10) ─────────────────────────────────────────────────────────

    {
        "owner": "bob", "category": "Creative",
        "title": "Guitar Lessons — Beginner to Intermediate",
        "description": (
            "Played guitar for 8 years, mostly indie and folk. I teach chords, strumming patterns, "
            "fingerpicking, and how to learn songs by ear. Bring your own acoustic or electric — "
            "I have a spare if you need one. Moody Hall practice rooms work great."
        ),
        "price": 20.00, "is_free": False, "contact_preference": "in_person",
        "contact_info": "Text 254-555-0182 to book a room", "availability_status": "available",
    },
    {
        "owner": "carol", "category": "Creative",
        "title": "Logo & Graphic Design Help",
        "description": (
            "CS major with a design hobby. I use Figma and Canva and can help you make flyers, "
            "club logos, presentation decks, or social media graphics. Tell me what you need "
            "and I'll get it done, usually within 48 hours. Free for student orgs."
        ),
        "price": None, "is_free": True, "contact_preference": "chat",
        "contact_info": "carol.chen on Discord", "availability_status": "available",
    },
    {
        "owner": "frank", "category": "Creative",
        "title": "Portrait & Event Photography",
        "description": (
            "Shot on a Sony A7III. I cover LinkedIn headshots, Greek life events, club officer "
            "photos, and casual portraits. I'll edit 15 final selects and deliver via Google Drive "
            "within 3 days. On-campus locations only. Outdoor or indoor — I bring my own lighting."
        ),
        "price": 30.00, "is_free": False, "contact_preference": "email",
        "contact_info": "frank@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "iris", "category": "Creative",
        "title": "Watercolor & Acrylic Painting Lessons",
        "description": (
            "Art major specializing in illustration. I'll teach you color mixing, brush control, "
            "composition, and how to develop your own style. Beginner-friendly — I supply materials "
            "for the first session. We meet at the Hooper-Schaefer Fine Arts building studio."
        ),
        "price": 15.00, "is_free": False, "contact_preference": "in_person",
        "contact_info": "iris@baylor.edu — come by studio 204", "availability_status": "available",
    },
    {
        "owner": "liam", "category": "Creative",
        "title": "Music Production & Beat Making",
        "description": (
            "I produce hip-hop and lo-fi beats in FL Studio and Ableton. I'll teach you the basics "
            "of DAW navigation, sound design, sampling, and mixing. Whether you want to make beats "
            "for fun or start releasing music, let's build your first track together."
        ),
        "price": 18.00, "is_free": False, "contact_preference": "chat",
        "contact_info": "liam.torres on Discord", "availability_status": "available",
    },
    {
        "owner": "quinn", "category": "Creative",
        "title": "Dance Lessons — Hip-Hop & Contemporary",
        "description": (
            "Dance team captain, 6 years of training. I teach beginner-friendly hip-hop, "
            "contemporary, and basic choreography. Great if you want to audition for a dance org, "
            "learn for fun, or just get more comfortable moving. Studio space available in the SLC."
        ),
        "price": None, "is_free": True, "contact_preference": "in_person",
        "contact_info": "SLC dance studio — DM @quinn.washington on Instagram to schedule",
        "availability_status": "available",
    },
    {
        "owner": "olivia", "category": "Creative",
        "title": "Podcast Editing & Audio Production",
        "description": (
            "I edit podcasts and voice-over projects using Audacity and Adobe Audition. "
            "I'll clean up your audio, remove background noise, add music/transitions, "
            "and export in any format you need. Turnaround 24-48 hours depending on length."
        ),
        "price": 12.00, "is_free": False, "contact_preference": "email",
        "contact_info": "olivia@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "iris", "category": "Creative",
        "title": "Digital Illustration & Character Design",
        "description": (
            "I work in Procreate and Illustrator. I can teach you the basics of digital illustration, "
            "or help you develop a character or mascot for your club or project. "
            "Portfolio available on request. iPad Pro + Apple Pencil recommended."
        ),
        "price": None, "is_free": True, "contact_preference": "chat",
        "contact_info": "iris.design on Instagram", "availability_status": "busy",
    },
    {
        "owner": "liam", "category": "Creative",
        "title": "Songwriting & Lyric Feedback",
        "description": (
            "Singer-songwriter with 4 released singles on Spotify. I'll workshop your lyrics, "
            "help you find a hook, suggest chord progressions, and give honest feedback on your "
            "song structure. Bring an acoustic guitar or just your lyrics and voice."
        ),
        "price": None, "is_free": True, "contact_preference": "in_person",
        "contact_info": "Moody Hall lobby — text 254-555-0193 to confirm time",
        "availability_status": "available",
    },
    {
        "owner": "frank", "category": "Creative",
        "title": "Video Editing — Reels, YouTube & Short Films",
        "description": (
            "I edit in Premiere Pro and DaVinci Resolve. I can help you cut a YouTube video, "
            "make polished Instagram reels, or edit a short film for class. "
            "Color grading, sound design, and captions included. Fast turnaround."
        ),
        "price": 20.00, "is_free": False, "contact_preference": "email",
        "contact_info": "frank@baylor.edu", "availability_status": "available",
    },

    # ── TECHNICAL (8) ─────────────────────────────────────────────────────────

    {
        "owner": "carol", "category": "Technical",
        "title": "Python Programming Help",
        "description": (
            "Junior CS major with internship experience. I help with assignments, debugging, "
            "data structures, algorithms, and personal projects. Comfortable with pandas, NumPy, "
            "Flask, and Django. Let's pair-program and get you unstuck."
        ),
        "price": None, "is_free": True, "contact_preference": "chat",
        "contact_info": "carol.chen on Discord", "availability_status": "available",
    },
    {
        "owner": "henry", "category": "Technical",
        "title": "Web Development — React & Node.js",
        "description": (
            "Full-stack dev with two internships. I can help you build a React app from scratch, "
            "set up a Node/Express backend, connect to a database, and deploy to Netlify or Render. "
            "Also comfortable with REST APIs, auth, and basic DevOps. Free first session."
        ),
        "price": 16.00, "is_free": False, "contact_preference": "chat",
        "contact_info": "henry.brooks on Discord", "availability_status": "available",
    },
    {
        "owner": "maya", "category": "Technical",
        "title": "Data Science & Machine Learning Help",
        "description": (
            "CS + Statistics double major. I help with data cleaning, EDA, scikit-learn models, "
            "Jupyter notebooks, and understanding results. Great for students in CIS 4350 or "
            "anyone doing a data-driven capstone. I speak plain English, not just equations."
        ),
        "price": 18.00, "is_free": False, "contact_preference": "email",
        "contact_info": "maya@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "peter", "category": "Technical",
        "title": "PC Building & Hardware Help",
        "description": (
            "Built 12 custom PCs, help people choose parts, troubleshoot issues, and upgrade "
            "existing setups. I can help you optimize for gaming, school work, or video editing "
            "on any budget. Free consultation — I'll tell you exactly what to buy."
        ),
        "price": None, "is_free": True, "contact_preference": "phone",
        "contact_info": "254-555-0207", "availability_status": "available",
    },
    {
        "owner": "henry", "category": "Technical",
        "title": "Git, GitHub & Command Line Basics",
        "description": (
            "Confused by git? I'll teach you branching, merging, pull requests, rebasing, "
            "and how to never lose your work again. Great for CS freshmen or anyone who's "
            "been avoiding version control. One session is usually enough to get comfortable."
        ),
        "price": None, "is_free": True, "contact_preference": "chat",
        "contact_info": "henry.brooks on Discord", "availability_status": "available",
    },
    {
        "owner": "maya", "category": "Technical",
        "title": "SQL & Database Design Tutoring",
        "description": (
            "I teach SQL from the ground up — SELECT, JOINs, subqueries, indexes, and schema design. "
            "Comfortable with PostgreSQL, MySQL, and SQLite. Also cover Django ORM basics if needed. "
            "Great for CIS 3340 students or anyone building a database-backed project."
        ),
        "price": 14.00, "is_free": False, "contact_preference": "email",
        "contact_info": "maya@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "alice", "category": "Technical",
        "title": "Excel & Data Analysis Tutoring",
        "description": (
            "VLOOKUP, pivot tables, charts, conditional formatting, and Power Query — I use Excel "
            "daily for my finance coursework. I can take you from confused to confident in one "
            "session. Great for BBA students or anyone doing research data."
        ),
        "price": None, "is_free": True, "contact_preference": "email",
        "contact_info": "alice@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "peter", "category": "Technical",
        "title": "Cybersecurity & CTF Help",
        "description": (
            "CompTIA Security+ certified. I help with network fundamentals, ethical hacking basics, "
            "CTF challenge walkthroughs, and understanding common vulnerabilities (OWASP Top 10). "
            "Great for anyone taking CIS 4360 or getting into security competitions."
        ),
        "price": 15.00, "is_free": False, "contact_preference": "chat",
        "contact_info": "p.andersen on Discord", "availability_status": "busy",
    },

    # ── LIFESTYLE (7) ─────────────────────────────────────────────────────────

    {
        "owner": "david", "category": "Lifestyle",
        "title": "Beginner Yoga — Campus Green Sessions",
        "description": (
            "Certified 200hr yoga teacher. I run casual 45-minute outdoor sessions on the campus "
            "green on Saturdays at 8am. All levels welcome — no experience needed, just bring a mat. "
            "Good for stress, posture, back pain, and flexibility. Free, donation-based."
        ),
        "price": None, "is_free": True, "contact_preference": "in_person",
        "contact_info": "Campus green, 8am Saturday — text 254-555-0147 if you have questions",
        "availability_status": "available",
    },
    {
        "owner": "tara", "category": "Lifestyle",
        "title": "Meditation & Stress Management Coaching",
        "description": (
            "Certified mindfulness instructor. I'll teach you breathwork, body scan, and "
            "focused attention techniques that actually work during finals. One 30-minute "
            "session is enough to learn three techniques you can use the same day."
        ),
        "price": None, "is_free": True, "contact_preference": "email",
        "contact_info": "tara@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "james", "category": "Lifestyle",
        "title": "Personal Training & Workout Programming",
        "description": (
            "NASM-certified personal trainer. I'll write you a custom 4-week program based on "
            "your goals (strength, fat loss, endurance) and coach you through your first few "
            "sessions at the Rec Center. No experience needed — form and safety first."
        ),
        "price": 20.00, "is_free": False, "contact_preference": "phone",
        "contact_info": "254-555-0219", "availability_status": "available",
    },
    {
        "owner": "noah", "category": "Lifestyle",
        "title": "Budget Meal Prep for Students",
        "description": (
            "Eating healthy on $50/week is totally doable — I've been doing it for 3 years. "
            "I'll build you a weekly meal plan, a Walmart shopping list, and walk you through "
            "4 core recipes that keep all week. One session, fully practical."
        ),
        "price": 8.00, "is_free": False, "contact_preference": "phone",
        "contact_info": "254-555-0228", "availability_status": "available",
    },
    {
        "owner": "eve", "category": "Lifestyle",
        "title": "Study Habit & Time Management Coaching",
        "description": (
            "Pre-med senior with a 3.9 GPA. I'll help you build a semester schedule, choose study "
            "techniques that match your learning style (flashcards vs active recall vs concept maps), "
            "and stop the procrastination cycle. First session is free."
        ),
        "price": None, "is_free": True, "contact_preference": "email",
        "contact_info": "eve@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "tara", "category": "Lifestyle",
        "title": "Resume Review & LinkedIn Optimization",
        "description": (
            "Interned at two Fortune 500s and helped 15+ students land their first internship. "
            "I'll review your resume, rewrite bullet points to be achievement-focused, and "
            "optimize your LinkedIn for recruiter searches. Usually takes one 1-hour session."
        ),
        "price": 10.00, "is_free": False, "contact_preference": "email",
        "contact_info": "tara@baylor.edu", "availability_status": "available",
    },
    {
        "owner": "james", "category": "Lifestyle",
        "title": "Running & Endurance Training Plans",
        "description": (
            "Cross-country runner, 5K PR of 16:42. I write customized weekly running plans "
            "for beginners or anyone training for a 5K, 10K, or half marathon. "
            "I'll also coach form, pacing strategy, and race-day nutrition. Free plan, just ask."
        ),
        "price": None, "is_free": True, "contact_preference": "email",
        "contact_info": "james@baylor.edu", "availability_status": "available",
    },
]

# ── Reviews ────────────────────────────────────────────────────────────────────
# (reviewer, skill_owner, title_hint, rating, comment)

REVIEWS = [
    ("carol",  "alice",  "Calculus",         5, "Alice explained limits in a way my professor never did. Passed my midterm with an 89!"),
    ("bob",    "carol",  "Python",            4, "Super patient and great at explaining. Helped me debug a project I'd been stuck on for days."),
    ("alice",  "bob",    "Guitar",            5, "Bob is a fantastic teacher. Learned 4 chords in the first session and was already playing a song."),
    ("david",  "alice",  "Calculus",          4, "Very clear explanations. She makes math feel approachable rather than terrifying."),
    ("eve",    "henry",  "React",             5, "Henry built an entire demo app while explaining every line. Best learning experience I've had."),
    ("alice",  "david",  "Yoga",              4, "Exactly what I needed during finals week. Low-key, welcoming, and helpful for my back pain."),
    ("carol",  "eve",    "Spanish",           5, "My pronunciation improved noticeably after two sessions. Eve is encouraging and fun."),
    ("bob",    "david",  "Yoga",              3, "Good session but the 8am Saturday time is rough. Would try again when the semester calms down."),
    ("henry",  "maya",   "Data Science",      5, "Maya walked me through my entire capstone dataset. Extremely knowledgeable and patient."),
    ("grace",  "kate",   "Chemistry",         5, "Kate is literally the reason I passed Gen Chem. She explains the intuition, not just the steps."),
    ("liam",   "frank",  "Photography",       4, "Great headshots, delivered ahead of schedule. Frank has a good eye for natural light."),
    ("iris",   "liam",   "Music Production",  5, "Made my first beat in the very first session. Liam explains everything in plain language."),
    ("james",  "tara",   "Resume",            5, "My resume went from a mess to something I'm actually proud to send. Got two callbacks that week."),
    ("noah",   "james",  "Personal Training", 4, "James wrote me a solid program and checked my form. I've been consistent for 6 weeks now."),
    ("olivia", "quinn",  "Dance",             5, "Quinn is so encouraging. I had zero confidence and now I actually want to audition for dance team."),
    ("tara",   "olivia", "Creative Writing",  4, "Olivia gave the most thoughtful feedback on my short story. She really gets voice and structure."),
    ("rachel", "grace",  "Biology",           5, "Grace made cell biology click for me in one session. Her diagrams and mnemonics are so helpful."),
    ("sam",    "rachel", "Psychology",        4, "Rachel knows her stuff and explains research methods in a way that actually makes sense."),
    ("peter",  "sam",    "Finance",           5, "Sam walked me through financial ratio analysis start to finish. Huge help for my FIN 3310 exam."),
    ("quinn",  "peter",  "PC Building",       4, "Peter helped me spec a PC for $800 that runs everything I need. No upselling, just solid advice."),
    ("maya",   "alice",  "Essay",             4, "Alice caught structural issues I completely missed. My argument is so much clearer now."),
    ("frank",  "iris",   "Watercolor",        5, "Iris is a gifted teacher. I had never painted before and left with something I'm actually proud of."),
    ("kate",   "noah",   "Meal Prep",         5, "Noah's meal plan saved me money and I stopped eating dining hall pizza every day. Life-changing."),
    ("rachel", "tara",   "Meditation",        5, "Tara's breathing technique is the only thing that got me through finals without a breakdown."),
    ("alice",  "henry",  "Git",               5, "Finally understand branches and PRs. Henry made it all make sense in under an hour."),
    ("carol",  "maya",   "SQL",               4, "Maya explained JOINs in three different ways until I got it. Very thorough and encouraging."),
    ("bob",    "frank",  "Video Editing",     4, "Frank turned my raw footage into a clean YouTube video. Delivered in 2 days."),
    ("david",  "james",  "Running",           5, "James wrote me a 5K training plan and I just ran my first race — 26:48. Couldn't have done it without him."),
    ("henry",  "peter",  "Cybersecurity",     4, "Helped me prep for a CTF competition. Peter knows his stuff and makes it accessible."),
    ("grace",  "olivia", "Podcast",           4, "Olivia cleaned up my podcast audio and added music that actually fits. Very professional result."),
]

# ── Booking Requests ───────────────────────────────────────────────────────────
# (requester, skill_owner, title_hint, message, status)

BOOKINGS = [
    ("bob",    "alice",  "Calculus",        "Hey Alice, I have an exam next Friday. Can we meet Wednesday evening?",                   "accepted"),
    ("david",  "carol",  "Python",          "I'm working on a data science project and could use help with pandas.",                   "pending"),
    ("carol",  "bob",    "Guitar",          "Always wanted to learn — is Saturday afternoon available?",                               "pending"),
    ("alice",  "david",  "Yoga",            "I'll be at the campus green Saturday. Looking forward to it!",                            "accepted"),
    ("liam",   "frank",  "Photography",     "Need a LinkedIn headshot before I apply to summer internships. When are you free?",       "accepted"),
    ("tara",   "quinn",  "Dance",           "I want to audition for the spring showcase — can you help me prep choreography?",         "pending"),
    ("henry",  "maya",   "Data Science",    "I need help understanding my capstone dataset. Can we do a 2-hour session this weekend?", "accepted"),
    ("grace",  "kate",   "Chemistry",       "Struggling with equilibrium. Can we meet before Thursday's lab?",                         "pending"),
    ("olivia", "liam",   "Music Production","I want to add a background track to my podcast. Is that something you can help with?",    "pending"),
    ("james",  "tara",   "Resume",          "Applying for internships next month. My resume is a mess — can you take a look?",         "accepted"),
    ("noah",   "james",  "Personal Training","I want to get stronger before the semester ends. Can we start this week?",               "pending"),
    ("peter",  "sam",    "Finance",         "FIN 3310 midterm is in two weeks and I don't understand ratios at all. Help!",            "pending"),
    ("quinn",  "iris",   "Watercolor",      "I want to make a gift for my mom's birthday. Can you help me paint something nice?",      "accepted"),
    ("rachel", "grace",  "Statistics",      "I need help interpreting my thesis regression output in SPSS. Pretty urgent.",             "pending"),
    ("sam",    "henry",  "React",           "Building a budgeting app for a hackathon. Need help with state management in React.",      "accepted"),
    ("maya",   "olivia", "Creative Writing","I've been writing a short story and need someone to give me honest feedback.",             "pending"),
    ("frank",  "carol",  "Logo",            "Our club needs a new logo for our T-shirts. Can you help design something?",              "accepted"),
    ("kate",   "tara",   "Meditation",      "Finals are destroying me. I need that 30-minute session ASAP.",                           "accepted"),
    ("iris",   "peter",  "PC Building",     "My laptop keeps overheating. Is that something you can diagnose?",                        "pending"),
    ("bob",    "henry",  "Git",             "I keep messing up merges on my team project. Can you show me how to fix conflicts?",      "accepted"),
]


class Command(BaseCommand):
    help = "Seed the database with 20 users, 35 skills, 30 reviews, and 20 booking requests."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Wipe all existing marketplace data before seeding.",
        )

    def handle(self, *args, **options):
        if Skill.objects.exists():
            if not options["reset"]:
                self.stdout.write(self.style.WARNING("Seed data already present — skipping."))
                self.stdout.write("  Re-run with --reset to wipe and replace all data.")
                return
            # --reset: delete all marketplace data, keep the admin superuser
            self.stdout.write(self.style.WARNING("--reset: wiping existing data..."))
            BookingRequest.objects.all().delete()
            Review.objects.all().delete()
            Skill.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write("  Existing data cleared.")

        self.stdout.write("Seeding database...")

        # ── Users ──────────────────────────────────────────────────────────────
        user_map = {}
        for u in USERS:
            obj, created = User.objects.get_or_create(
                username=u["username"],
                defaults={
                    "email":      u["email"],
                    "first_name": u["first_name"],
                    "last_name":  u["last_name"],
                },
            )
            if created:
                obj.set_password(u["password"])
                obj.save()
            user_map[u["username"]] = obj
        self.stdout.write(f"  + {len(user_map)} users")

        # ── Skills ─────────────────────────────────────────────────────────────
        skill_map = {}
        for s in SKILLS:
            skill = Skill.objects.create(
                owner=user_map[s["owner"]],
                title=s["title"],
                description=s["description"],
                category=s["category"],
                price=s["price"],
                is_free=s["is_free"],
                contact_preference=s["contact_preference"],
                contact_info=s["contact_info"],
                availability_status=s["availability_status"],
                active=True,
            )
            skill_map[(s["owner"], s["title"])] = skill
        self.stdout.write(f"  + {len(SKILLS)} skills")

        # ── Reviews ────────────────────────────────────────────────────────────
        review_count = 0
        for reviewer_u, owner_u, title_hint, rating, comment in REVIEWS:
            reviewer = user_map.get(reviewer_u)
            skill = next(
                (v for (o, t), v in skill_map.items() if o == owner_u and title_hint in t),
                None,
            )
            if skill and reviewer and not Review.objects.filter(skill=skill, reviewer=reviewer).exists():
                Review.objects.create(skill=skill, reviewer=reviewer, rating=rating, comment=comment)
                review_count += 1
        self.stdout.write(f"  + {review_count} reviews")

        # ── Booking requests ───────────────────────────────────────────────────
        booking_count = 0
        for requester_u, owner_u, title_hint, message, status in BOOKINGS:
            requester = user_map.get(requester_u)
            skill = next(
                (v for (o, t), v in skill_map.items() if o == owner_u and title_hint in t),
                None,
            )
            if skill and requester and not BookingRequest.objects.filter(skill=skill, requester=requester).exists():
                BookingRequest.objects.create(skill=skill, requester=requester, message=message, status=status)
                booking_count += 1
        self.stdout.write(f"  + {booking_count} booking requests")

        self.stdout.write(self.style.SUCCESS("\nDatabase seeded successfully!"))
        self.stdout.write("  All 20 accounts use password: skillswap2024")
        self.stdout.write("  Try logging in as: alice, bob, carol, david, henry, maya, ...")
