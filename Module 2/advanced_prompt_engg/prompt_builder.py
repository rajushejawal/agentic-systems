You have just learned the three most powerful advanced prompting techniques: Chain-of-Thought (CoT), Structured Prompts, and Reasoning Prompts. Now it is time to move from understanding to building.

Your task is to build a Python-based Prompt Builder for a real-world AI agent use case of your choice from the list below:

Choose ONE agent to build a prompt for:

A Mock Interview Agent — helps students prepare for data/AI job interviews by asking questions and giving structured feedback
# A Code Review Agent — reviews a Python code snippet and provides feedback on bugs, readability, and improvements
# A Product Launch Advisor Agent — evaluates whether a new product idea is ready to launch, giving a GO/NO-GO recommendation

What You Must Build (in this Python file):
Part 1 — Structured Prompt Builder Function

Write a Python function called build_agent_prompt(...) that:

Accepts at least 2 dynamic input parameters relevant to your chosen agent (e.g., user background, product description, code snippet)
Constructs a complete Structured Prompt using all 5 components as separate variables:
role — Give the agent a name and at least 2 specific personality traits
task — One clear sentence defining the agent's deliverable
instructions — At least 4 numbered steps that embed Chain-of-Thought reasoning (the agent must follow these steps before responding)
constraints — At least 3 guardrails written as positive instructions (what the agent MUST do, not what it must NOT do — apply Best Practice #2)
output_format — Clearly specify sections, headers, or structure of the expected response
Combines all components using an f-string into a single full_prompt string
Returns full_prompt





# Part 2 — Reasoning Prompt Section

# Inside the same file, write a separate string variable called reasoning_prompt that demonstrates one of the three Reasoning Prompt types (Comparison, Causal, or Decision-Making) — relevant to your agent's domain. This should be a standalone prompt (not inside the function), showing criteria-based evaluation and a request for a final recommendation.

# Part 3 — Demonstration

# At the bottom of the file:

# Call build_agent_prompt(...) with two different sets of inputs (simulate two different users or scenarios)
# Print both outputs with clear separator lines
# Add a print statement that outputs the character count of each generated prompt (for token cost awareness)




# # Your Prompt Builder should include the following components:
# # 1. **Agent Description**: A brief description of the agent's purpose and functionality.
# # 2. **Prompt Template**: A structured prompt template that includes placeholders for user input and instructions for the agent.
# # 3. **Example Usage**: A sample interaction with the agent, demonstrating how the prompt is filled out and how the agent responds.
# # Here is an example of how you might structure your Prompt Builder for the Mock Interview Agent:

# # ```pythonclass 
# class MockInterviewAgent:
#     def __init__(self):
#         self.description = "A Mock Interview Agent that helps students prepare for data/AI job interviews by asking questions and giving structured feedback."
#         self.prompt_template = """
#         You are a Mock Interview Agent. Your task is to ask the user a series of interview questions based on the following topic: {topic}.
        
#         After the user answers each question, provide structured feedback on their response, including:
#         1. Strengths: What did they do well?
#         2. Areas for Improvement: What could they improve?
#         3. Additional Resources: Suggest resources for further study.
        
#         Please start by asking the first question.
#         """

#     def generate_prompt(self, topic):
#         return self.prompt_template.format(topic=topic)
#         # Example Usage
#         if __name__ == "__main__":
#             agent = MockInterviewAgent()
#             topic = "Data Structures and Algorithms"
#             prompt = agent.generate_prompt(topic)
#             print("Agent Description:")
#             print(agent.description)
#             print("\nGenerated Prompt:")
#             print(prompt)
# # ```
# # You can follow a similar structure for the Code Review Agent and the Product Launch Advisor Agent, tailoring the prompt template and feedback structure to fit the specific use case.
# # Here is an example of how you might structure your Prompt Builder for the Code Review Agent:


# class CodeReviewAgent:
#     def __init__(self):
#         self.description = "A Code Review Agent that reviews a Python code snippet and provides feedback on bugs, readability, and improvements."
#         self.prompt_template = """
#         You are a Code Review Agent. Your task is to review the following Python code snippet and provide feedback on the following aspects:
        
#         1. Bugs: Identify any potential bugs or issues in the code.
#         2. Readability: Assess the readability of the code and suggest improvements.
#         3. Improvements: Provide suggestions for improving the code's efficiency or style.
        
#         Here is the code snippet:
#         {code_snippet}
        
#         Please provide your feedback based on the criteria above.
#         """

#     def generate_prompt(self, code_snippet):
#         return self.prompt_template.format(code_snippet=code_snippet)
#     # Example Usage
#     if __name__ == "__main__":
#         agent = CodeReviewAgent()
#         code_snippet = """def factorial(n):
#         if n == 0:
#             return 1
#         else:
#             return n * factorial(n-1)"""
#         prompt = agent.generate_prompt(code_snippet)
#         print("Agent Description:")
#         print(agent.description)
#         print("\nGenerated Prompt:")
#         print(prompt)

# # ```And here is an example of how you might structure your Prompt Builder for the Product Launch Advisor Agent:

# # ```python
# # 
# class ProductLaunchAdvisorAgent:
#     def __init__(self):
#         self.description = "A Product Launch Advisor Agent that evaluates whether a new product idea is ready to launch, giving a GO/NO-GO recommendation."
#         self.prompt_template = """
#         You are a Product Launch Advisor Agent. Your task is to evaluate the following product idea and provide a GO/NO-GO recommendation based on the following criteria:
        
#         1. Market Fit: Does the product address a clear market need?
#         2. Competitive Analysis: How does the product compare to existing solutions?
#         3. Feasibility: Is the product technically and financially feasible to launch?
        
#         Here is the product idea:
#         {product_idea}
        
#         Please provide your evaluation and recommendation based on the criteria above.
#         """

# def generate_prompt(self, product_idea):
#     return self.prompt_template.format(product_idea=product_idea)             
# # Example Usage 
#     if __name__ == "__main__":
#         agent = ProductLaunchAdvisorAgent()
#         product_idea = "A mobile app that helps users track their daily water intake and provides personalized hydration recommendations."
#         prompt = agent.generate_prompt(product_idea)
#         print("Agent Description:")
#         print(agent.description)
#         print("\nGenerated Prompt:")
#         print(prompt)
# # ```
# # You can choose to implement one of the agents above or create your own agent based on a different use case. The key is to ensure that your Prompt Builder includes a clear agent description, a structured prompt template, and an example usage that demonstrates how the prompt is generated and used.
