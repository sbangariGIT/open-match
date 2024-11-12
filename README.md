# OPEN MATCH

## Inspiration

Contributing to open source is an incredible way to grow as a developer, enhance your skills, and make a positive impact on the tech community. However, for many of us, especially first-timers, the journey can feel daunting. With countless projects and issues to sift through, it’s often overwhelming to find the right fit. Despite the availability of platforms that list open issues, there remains a steep learning curve to navigate complex codebases and identify tasks that align with one's expertise.

That's where Open-Match comes in. Our mission is to empower developers to make impactful open-source contributions by simplifying this process. By allowing users to upload their profiles, we are trying to match them with open issues that align with their existing skills and interests. We aim to reduce the friction of that first contribution, helping developers discover where their talents can truly make a difference. Open-Match is here to bridge the gap between developers and the open-source projects that need their unique skills, making it easier for everyone to get started and grow in the world of open-source.

## 🛠️ How We Built Open-Match
Open-Match is built with a focus on delivering a seamless experience for developers looking to make impactful open-source contributions. Here's an overview of how we developed the project:

### Frontend
The frontend allows developers to upload their resumes, LinkedIn profiles, GitHub profiles, and other relevant information. This data is used to understand the user’s skills, experience, and interests, which helps us create personalized recommendations for open-source issues.

### Backend & Data Processing
At the core of our backend, we developed a service that indexes open GitHub issues. This service uses the GitHub API to fetch and update our database of open issues, ensuring that it stays up-to-date with the latest contributions and projects. To make this data more insightful, we leverage Large Language Models (LLMs) to generate comprehensive summaries of each issue, making it easier to understand the context and requirements.

### Matching Engine
To match developers with the most suitable issues, we implemented a semantic search engine using MongoDB Atlas. We use LLMs to generate semantic embeddings of both developer profiles and GitHub issues. This allows us to perform a highly accurate matching based on the relevance of a user's skills and experience to the open issues. By using this approach, we go beyond simple keyword matching, ensuring that users are presented with issues where their contributions can have the most impact.

### Bringing It All Together
The result is a streamlined platform that empowers developers to quickly discover open-source projects that align with their skills and passions. Whether you're a seasoned contributor or someone making their first open-source contribution, Open-Match is designed to help you find your perfect match and start making meaningful contributions right away.

