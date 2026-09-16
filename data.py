"""
All portfolio content lives here as plain Python data structures.
Edit this file to update your info -- you never need to touch the HTML templates
just to change text, add a project, or write a new blog post.
"""

PROFILE = {
    "name": "Palak Jangir",
    "role": "Full-Stack Developer -- AI & Data Systems",
    "phone": "7742404929",
    "email": "jangirpalak1996@gmail.com",
    "linkedin_label": "palak-jangir-14763822b",
    "linkedin_url": "https://www.linkedin.com/in/palak-jangir-14763822b",
    "github_url": "https://github.com/Palak28-web",
    "summary": (
        "I like turning messy problems into things that actually work.\n Lately that's meant teaching chatbots to answer real questions,\n wiring up dashboards that make sense of mountains of data,\n and building full-stack apps that don't fall over in production.\n I love turning ideas into things people can actually use—from full-stack\n applications to AI-powered experiences.\n Currently doing this at Accenture —\n always up for the next interesting problem. \n I build with React, Flask, cloud technologies, and data,\n exploring everything from RAG and LLMs to scalable APIs and analytics.\n"
    ),
}

EDUCATION = [
    {
        "school": "Malviya National Institute of Technology, Jaipur",
        "detail": "B.Tech., CGPA: 9.02/10",
        "years": "2021 -- 2025",
    },
    {
        "school": "Aakash Career Institute, Jhunjhunu",
        "detail": "RBSE 12th Examination -- 99.40% aggregate",
        "years": "2021",
    },
    {
        "school": "Shri Gangaram Balkishan Modi Public School",
        "detail": "RBSE 10th Examination -- 93.67% aggregate",
        "years": "2019",
    },
]

EXPERIENCE = [
    {
        "role": "Advanced Application Engineer",
        "company": "Accenture",
        "years": "Oct 2025 -- Present",
        "points": [
            "Developed and integrated a Retrieval-Augmented Generation (RAG) pipeline using LLMs.",
            "Built full-stack applications with React and Flask, leveraging AWS Lex for chatbot functionality.",
            "Designed RESTful APIs and data workflows, applying prompt engineering to improve model responses.",
            "Deployed solutions on Azure Web Apps and Function Apps for scalability and high availability.",
            "Integrated the Bright Data API for large-scale data collection and processing.",
            "Used Google BigQuery to query large datasets efficiently, cutting analysis time significantly.",
            "Built an interactive analytics dashboard in Looker Studio for real-time stakeholder insights.",
        ],
    },
    {
        "role": "Software Developer Intern",
        "company": "Vegavid Technology Private Limited",
        "years": "May 2024 -- Jul 2024",
        "points": [
            "Built a subscription-based MERN application with secure JWT authentication and Stripe payments.",
            "Implemented automated email notifications via Mailjet and improved UX with React Toastify.",
            "Designed test cases and generated coverage reports for reliable software delivery.",
        ],
    },
]

SKILLS = [
    {
        "category": "Programming Languages",
        "items": ["C", "C++", "Python", "Java", "JavaScript"],
    },
    {
        "category": "Web Development",
        "items": [
            "HTML", "CSS", "Bootstrap", "React.js", "Next.js", "Material UI",
            "Node.js", "Express.js", "Python Flask", "REST API Design",
            "Authentication & Authorization", "JWT", "SSO",
        ],
    },
    {
        "category": "Databases",
        "items": ["MongoDB", "MySQL"],
    },
    {
        "category": "AI, Data & Backend",
        "items": [
            "Retrieval-Augmented Generation (RAG)", "Large Language Models (LLMs)",
            "Prompt Engineering", "API Integration", "Document/PDF Parsing",
            "Bright Data", "Google BigQuery", "SQL",
        ],
    },
    {
        "category": "DevOps & Cloud",
        "items": ["AWS", "Kubernetes", "CI/CD Pipelines", "Docker", "AWS Cloud Fundamentals", "YAML"],
    },
    {
        "category": "Tools",
        "items": ["Git", "GitHub", "GitLab", "Postman"],
    },
]

PROJECTS = [
    {
        "slug": "chicago-crime-dashboard",
        "title": "Chicago Crime Data Analysis Dashboard",
        "tagline": "A Flask + MySQL analytics dashboard over Chicago's public crime data.",
        "description": (
            "A web-based analytics dashboard built with Python, Flask, Pandas, MySQL, and "
            "data-visualization libraries. Implements a complete ingestion pipeline -- from raw "
            "CSV ingestion and cleaning through to structured storage in MySQL -- enabling fast, "
            "reliable querying over a large public safety dataset."
        ),
        "highlights": [
            "Built a full CSV-to-MySQL ingestion pipeline with cleaning and validation.",
            "Structured storage for faster, indexed querying of crime records.",
            "Visualized trends and patterns for exploratory analysis.",
        ],
        "tech": ["Python", "Flask", "Pandas", "MySQL"],
        "link": "https://github.com/Palak28-web/chicago",
        "link_label": "View on GitHub",
    },
]

BLOG_POSTS = [
    {
        "slug": "building-rag-pipelines",
        "title": "What I learned building a RAG pipeline in production",
        "date": "2026-02-14",
        "excerpt": (
            "Notes from wiring retrieval-augmented generation into a real Flask backend -- "
            "chunking strategy, prompt design, and the failure modes nobody warns you about."
        ),
        "body": [
            "This is a placeholder post -- replace it with your own write-up. A good structure "
            "for a technical post like this is: the problem you were solving, the approach you "
            "took, what worked, and what you'd do differently next time.",
            "Talk about chunking strategy, embedding choice, and how you evaluated retrieval "
            "quality. Concrete numbers and code snippets make posts like this far more useful "
            "to future-you and to readers.",
        ],
    },
    {
        "slug": "flask-to-production",
        "title": "Taking a Flask side project from laptop to Azure",
        "date": "2026-01-03",
        "excerpt": (
            "A short checklist for deploying a Flask app to Azure Web Apps without the usual "
            "3am surprises."
        ),
        "body": [
            "Another placeholder -- swap this out for a real post. Consider covering: "
            "environment variables and secrets, WSGI server choice (gunicorn), health checks, "
            "and how you set up CI/CD for the deploy.",
        ],
    },
]

EXTRAS = [
    "Organized Chemical Department Day 2024, coordinating 200+ participants and managing logistics.",
    "Executive on the decor team for Chemical Department Day, 2022 and 2023.",
    "Member of the Computer Science Club, Creative Arts Club, and Mess Committee.",
]
