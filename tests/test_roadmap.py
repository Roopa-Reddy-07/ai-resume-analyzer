from roadmap_generator import generate_learning_roadmap


missing_skills = [
    "machine learning",
    "scikit-learn",
    "pytorch",
    "fastapi",
    "docker"
]


roadmap = generate_learning_roadmap(
    missing_skills
)


print("\n----- LEARNING ROADMAP -----\n")

for item in roadmap:

    print(
        f"Week {item['week']}: "
        f"{item['topic']}"
    )

    print(
        f"   → {item['resource']}\n"
    )