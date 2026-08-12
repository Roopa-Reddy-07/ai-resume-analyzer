ROADMAP = {
    "python": {
        "topic": "Python Programming",
        "resource": "Practice Python fundamentals, functions, OOP, modules, and file handling."
    },
    "sql": {
        "topic": "SQL",
        "resource": "Learn SELECT, JOIN, GROUP BY, subqueries, and database design."
    },
    "pandas": {
        "topic": "Pandas",
        "resource": "Learn DataFrames, data cleaning, filtering, grouping, merging, and aggregation."
    },
    "numpy": {
        "topic": "NumPy",
        "resource": "Learn arrays, indexing, broadcasting, mathematical operations, and numerical computing."
    },
    "machine learning": {
        "topic": "Machine Learning Fundamentals",
        "resource": "Study supervised learning, regression, classification, model evaluation, and feature engineering."
    },
    "scikit-learn": {
        "topic": "Scikit-learn",
        "resource": "Practice preprocessing, pipelines, model training, evaluation, and hyperparameter tuning."
    },
    "tensorflow": {
        "topic": "TensorFlow",
        "resource": "Learn neural networks, model training, validation, and TensorFlow workflows."
    },
    "pytorch": {
        "topic": "PyTorch",
        "resource": "Learn tensors, datasets, neural networks, training loops, and model evaluation."
    },
    "deep learning": {
        "topic": "Deep Learning",
        "resource": "Study neural networks, CNNs, optimization, regularization, and model evaluation."
    },
    "nlp": {
        "topic": "Natural Language Processing",
        "resource": "Learn text preprocessing, tokenization, embeddings, classification, and language models."
    },
    "transformers": {
        "topic": "Transformers",
        "resource": "Learn attention mechanisms, transformer architecture, and transformer-based NLP models."
    },
    "hugging face": {
        "topic": "Hugging Face",
        "resource": "Practice using pretrained models, tokenizers, pipelines, and model fine-tuning."
    },
    "llm": {
        "topic": "Large Language Models",
        "resource": "Learn LLM concepts, prompting, model APIs, embeddings, and practical applications."
    },
    "rag": {
        "topic": "Retrieval Augmented Generation",
        "resource": "Learn embeddings, vector databases, retrieval, and context-aware generation."
    },
    "opencv": {
        "topic": "OpenCV",
        "resource": "Learn image processing, image transformations, feature detection, and computer vision workflows."
    },
    "cnn": {
        "topic": "Convolutional Neural Networks",
        "resource": "Learn convolution, pooling, feature maps, image classification, and CNN architectures."
    },
    "yolo": {
        "topic": "YOLO Object Detection",
        "resource": "Learn object detection, bounding boxes, datasets, training, and inference using YOLO."
    },
    "computer vision": {
        "topic": "Computer Vision",
        "resource": "Study image processing, classification, object detection, and visual recognition."
    },
    "flask": {
        "topic": "Flask",
        "resource": "Learn Flask routes, templates, forms, APIs, and backend application development."
    },
    "fastapi": {
        "topic": "FastAPI",
        "resource": "Learn API creation, request validation, endpoints, and deploying Python APIs."
    },
    "rest api": {
        "topic": "REST APIs",
        "resource": "Learn HTTP methods, REST architecture, JSON, API requests, and API design."
    },
    "docker": {
        "topic": "Docker Fundamentals",
        "resource": "Learn containers, Dockerfiles, images, containers, volumes, and basic deployment."
    },
    "kubernetes": {
        "topic": "Kubernetes",
        "resource": "Learn pods, deployments, services, scaling, and container orchestration."
    },
    "aws": {
        "topic": "AWS Fundamentals",
        "resource": "Learn core AWS services, compute, storage, networking, and basic cloud deployment."
    },
    "azure": {
        "topic": "Microsoft Azure",
        "resource": "Learn Azure compute, storage, networking, and application deployment."
    },
    "git": {
        "topic": "Git",
        "resource": "Practice repositories, commits, branches, merging, and collaborative workflows."
    },
    "github": {
        "topic": "GitHub",
        "resource": "Learn repositories, pull requests, issues, GitHub workflows, and project collaboration."
    },
    "html": {
        "topic": "HTML",
        "resource": "Learn semantic HTML, forms, tables, accessibility, and page structure."
    },
    "css": {
        "topic": "CSS",
        "resource": "Learn selectors, layouts, Flexbox, Grid, responsive design, and styling."
    },
    "javascript": {
        "topic": "JavaScript",
        "resource": "Learn variables, functions, DOM manipulation, asynchronous programming, and modern JavaScript."
    },
    "react": {
        "topic": "React",
        "resource": "Learn components, props, state, hooks, routing, and API integration."
    },
    "nodejs": {
        "topic": "Node.js",
        "resource": "Learn Node.js, npm, backend development, APIs, and asynchronous programming."
    },
    "mongodb": {
        "topic": "MongoDB",
        "resource": "Learn collections, documents, CRUD operations, queries, and database design."
    },
    "mysql": {
        "topic": "MySQL",
        "resource": "Practice relational database design, SQL queries, joins, and database management."
    },
    "postgresql": {
        "topic": "PostgreSQL",
        "resource": "Learn PostgreSQL queries, relational design, indexing, and database management."
    },
    "power bi": {
        "topic": "Power BI",
        "resource": "Learn data import, transformations, dashboards, visualizations, and DAX basics."
    },
    "tableau": {
        "topic": "Tableau",
        "resource": "Learn dashboards, data visualization, filters, calculated fields, and storytelling."
    },
    "excel": {
        "topic": "Advanced Excel",
        "resource": "Practice formulas, pivot tables, charts, lookups, and data analysis."
    },
    "statistics": {
        "topic": "Statistics",
        "resource": "Study probability, distributions, hypothesis testing, correlation, and regression."
    }
}


def generate_learning_roadmap(missing_skills):
    """
    Generate a simple weekly learning roadmap
    based on missing skills.
    """

    roadmap = []

    for index, skill in enumerate(missing_skills):

        skill = skill.lower().strip()

        if skill in ROADMAP:
            roadmap.append({
                "week": index + 1,
                "skill": skill,
                "topic": ROADMAP[skill]["topic"],
                "resource": ROADMAP[skill]["resource"]
            })
        else:
            roadmap.append({
                "week": index + 1,
                "skill": skill,
                "topic": skill.title(),
                "resource": f"Learn the fundamentals and practice {skill.title()} through a small project."
            })

    return roadmap