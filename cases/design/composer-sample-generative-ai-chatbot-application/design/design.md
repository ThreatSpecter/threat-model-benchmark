# Sample Generative AI Chatbot Application 



### Disclaimers

_**1. Motivation for externalizing this threat model:**_

_This example threat model for a 'Generative AI Chatbot Application' is informational only and provided "as is" with no representations or warranties whatsoever, and may change at any time due to a variety of factors, such as changes to AWS's services.  The provision of this example threat model does not create any warranties, representations, contractual commitments, conditions or assurances from AWS, its affiliates, suppliers or licensors. We've included this example threat model to show how you could use Threat Composer to create a threat model. This example threat model is a proof of concept and is not suitable for every possible interaction or use case. It aims to give the reader an example of what a set of threats, assumptions and mitigations could look like. We've chosen to share this example as it provides a common reference point for people who are starting off with a 'Generative AI Chatbot Application'. You may have different perspectives on the assumptions, threats, mitigations and prioritization. This is ok, and could be used to start conversations in your organization within the context of your risk appetite. You may want to use this example threat model as the base threat model or starting point to generate a contextualised threat model for your own specific needs and deployment of a 'Generative AI Chatbot Application'. This example threat model uses a reference architecture and is not a complete end-to-end solution. You are solely responsible for making your own independent assessment of this example threat model and its applicability to your organization._

_**2. Source used**_

_This example threat model based is on industry standards like the [Open Worldwide Application Security Project (OWASP) Top 10 for Large Language Models](https://owasp.org/www-project-top-10-for-large-language-model-applications/),  [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) and [AWS AWS Security Reference Architecture For Generative AI
](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/generative-ai.html)_

_**3. Criteria for prioritizing threats**_

_In this example threat model, the (hypothetical) chat-bot operator has explicitly determined that confidentiality of question-and-answer retrieval augmented generation (RAG) is their highest security priority. The chat-bot operator has determined that data integrity (and quality) of inference responses is of moderate security priority due to company training, and additional process controls to ensure chatbot users understand that responses may include inaccuracies and hallucinations. The chat-bot operator determined that availability of their service to be lowest-priority, as they are able to point users to other operational resources if the chat bot functionality has a service availability or degradation lasting several hours to a few days. Please note, these are examples of priorities based on which property ([C/I/A](https://www.nist.gov/image/cia-triad)) they impact. Customers should calculate priority using their own factors as part of any internal risk frameworks._

_**4. Agreement**_

_All use of AWS's services will be governed by the AWS Customer Agreement available at http://aws.amazon.com/agreement/ (or other definitive written agreement as may be agreed between the parties governing the use of AWS's services). If you use any artificial intelligence and machine learning Services, features, and functionality (including third-party models) that we provide, you will comply with the AWS Responsible AI Policy._

### Summary

This example threat model leverages a large language model (LLM) available in [Amazon Bedrock](https://aws.amazon.com/bedrock/) for natural language processing and other capacities, with the aim to deliver an intelligent conversational assistant. The example threat model is intended to  provide rapid, relevant responses to customer questions across diverse use cases like customer service, sales, and e-commerce. Integration with the [LangChain](https://www.langchain.com/)  framework can enable continuity by recalling previous interactions for personalized follow-ups. The goal is to provide an intelligent chatbot to transform customer experiences.

Previous generations of chatbots needed to be programmed for every possible customer interaction. But chatbots powered by LLMs that can access relevant documents can provide more natural conversations. These chatbots and virtual assistants are transforming customer engagements by understanding questions and responding swiftly. Backed by natural language processing and machine learning, the chatbots address customer queries across domains like customer service, sales, and e-commerce. This example threat modelutilizes Amazon Bedrock and other AWS services to boost chatbot capabilities. It offers configurations like basic, prompt-based, persona-based, and context-aware. The focus is delivering smooth, intelligent interactions to delight customers.

### Features

- Integration with Amazon Bedrock for advanced conversational capabilities
- Integration with Amazon Bedrock Guardrails for Responsible AI moderation
- LangChain framework for tracking chat history and context
- Flexible chatbot configurations: basic, prompt-based, persona, context-aware
- Workflow to embed user query, enable contextual search, provide relevant results
- Easy setup using Amazon Bedrock boto3 notebook
- Core natural language processing and machine learning
- Deployable across customer service, sales, and e-commerce etc.
- Integrates across websites, social media, and messaging platforms
- Focuses on contextual, personalized interactions
- Continued innovation for more natural conversations

### Sample architecture and documentation:

- Multi-Model and Multi-RAG Powered Chatbot CDK project, source code available [here](https://github.com/aws-samples/aws-genai-llm-chatbot/tree/main)
- Bedrock Claude Chat project, source code available [here](https://github.com/aws-samples/bedrock-claude-chat)
- A chatbot workshop and source code available [here](https://github.com/aws-samples/amazon-bedrock-workshop/blob/main/04_Chatbot/README.md#lab-4---conversational-interfaces-chatbots)
- Machine Learning Blog on how to use Retrieval Augmented Generation (RAG) is available [here](https://aws.amazon.com/blogs/machine-learning/simplify-access-to-internal-information-using-retrieval-augmented-generation-and-langchain-agents/)

## Architecture

This document outlines a sample reference architecture for an AI-powered assistant designed to provide rapid, accurate responses to queries about internal data. By leveraging AWS services, particularly [Amazon Bedrock](https://aws.amazon.com/bedrock/), this reference architecture demonstrates a secure, efficient, and intelligent solution for accessing organizational knowledge.

#### Key Benefits

- **Accelerated Insights**: The system generates instant answers from internal documents using Amazon Bedrock models.
- **Convenient Knowledge Access**: Users access information across various internal sources through a centralized interface.
- **Improved Productivity**: The architecture significantly reduces time spent on manual document searches.
- **Natural Interactions**: Amazon Bedrock powers a conversational interface for an intuitive user experience.
- **Historical Lookup**: A centralized dashboard enables review of past queries and answers.
- **Enhanced Security and Compliance**: The architecture implements responsible AI practices and robust data protection.

#### Architecture Components

#### 1. Data Preparation Pipeline

- **[Amazon S3](https://aws.amazon.com/s3/)**: Stores the knowledge base data.
- **Amazon S3 Event Trigger**: Initiates processing for new or updated objects.
- **[AWS Lambda](https://aws.amazon.com/lambda/)**: Parses data, converts to embeddings, and loads into vector database.
- **[Amazon Bedrock (Titan Embedding Model)](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)**: Generates embeddings for efficient data retrieval. This model is crucial for Retrieval-Augmented Generation (RAG), enabling the system to efficiently search and retrieve relevant information from the knowledge base.

#### 2. Application Stack

##### Frontend and Request Handling
- **[Amazon Cognito](https://aws.amazon.com/cognito/)**: Manages user authentication.
- **[AWS WAF](https://aws.amazon.com/waf/)**: Provides web application firewall protection.
- **Application Load Balancer**: Routes requests in the public subnet.
- **[Amazon ECS](https://aws.amazon.com/ecs/) with Fargate**: Hosts the NextJS Web Application (Docker).
- **AWS Lambda Web Adapter (Python)**: Handles serverless processing.

##### Backend Services
- **[Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/)**: Serves as the vector database for efficient document search.
- **[Amazon Bedrock Guardrail](https://aws.amazon.com/bedrock/guardrails/)**: Performs responsible AI checks and PII redaction.
- **[Amazon Bedrock (Anthropic Claude Model)](https://aws.amazon.com/bedrock/claude/)**: Powers natural language understanding and response generation.
- **[Amazon DynamoDB](https://aws.amazon.com/dynamodb/)**: Stores chat history for future reference.

##### Networking and Security
- **[Amazon VPC](https://aws.amazon.com/vpc/)**: Enhances overall system security through proper network design.
- **VPC Service Endpoints**: Connect the application securely to Bedrock, OpenSearch, and DynamoDB within the VPC.

#### Workflow

1. Users submit queries through the web application.
2. The system authenticates requests using Amazon Cognito and routes them through AWS WAF and the Application Load Balancer.
3. The NextJS Web Application in ECS processes the request, utilizing the AWS Lambda Web Adapter for serverless capabilities.
4. The architecture searches the OpenSearch Serverless vector database for relevant information.
5. Amazon Bedrock Guardrail applies responsible AI checks and PII redaction.
6. The Anthropic Claude Model in Amazon Bedrock generates a natural language response.
7. The system returns the answer to the user through the application stack and logs the interaction in DynamoDB.

#### Key Features

- Implementation of Amazon Bedrock Guardrail for PII redaction and responsible AI enforcement.
- Utilization of a serverless architecture with ECS Fargate and Lambda for scalability and performance.
- Integration of security measures through VPC design and AWS WAF.
- Application of advanced AI models, including the Titan Embedding Model for RAG and the Anthropic Claude Model for natural language processing.


***Disclaimer:*** _This document describes a sample reference architecture. Actual implementation may require adjustments based on specific organizational needs, security requirements, and compliance standards._


## Data flow

The data flows provide an in-depth look at how RAG chatbots operate. They outline the key processes and interactions that bring natural conversations to life. In below example, sample AWS services are used, you may or maybe not be using these services. 

#### Entities:

| Entity | Description |
|-|-|  
| User | The individual who interacts with the system |
| Web App | The frontend interface for input and output |
| Amazon Cognito | Handles user authentication |
| API Gateway | Orchestrates API requests and responses |
| Lambda| Serverless functions interacting with services |
| Amazon Bedrock Guardrail | Performs responsible AI check and PII redaction |
| OpenSearch Serverless| Retrieves relevant documents |
| Amazon Bedrock | Generates responses to queries |
| DynamoDB | Stores question-answer pairs |

#### Data flows definition:

| Flow Identifier | Flow Description | Source Entity | Target Entity | Assets |
|-|-|-|-|-|  
| DF1 | User asks a question | User | Web App | User supplied prompt |
| DF2 | Query is authenticated | Web App | Amazon Cognito | Credentials + Authentication tokens |   
| DF3 | API request handled | Web App | API Gateway | User supplied prompt, Authentication tokens|
| DF4 | Lambda function triggered | API Gateway | Lambda | User supplied prompt, LLM response |
| DF5 | Responsible AI check and PII redaction | Lambda | Amazon Bedrock Guardrail | Unredacted user supplied prompt, Redacted prompts, Intellectual property, Sensitive data |
| DF6 | Relevant documents retrieved | Lambda | OpenSearch Serverless | Intellectual property, Sensitive data |
| DF7 | Response generated | Lambda | Amazon Bedrock | User supplied prompt, LLM response  |
| DF8 | Generated response returned | Amazon Bedrock | Lambda | LLM response |  
| DF9 | Q and A stored | Lambda | DynamoDB | User supplied prompt, LLM responses, Audit log |


#### Trust boundaries:

| Boundary Identifier | Purpose | Source Entity | Target Entity |
|-|-|-|-|
| TB1 | Validates input, ensures privacy | User | Web App |
| TB2 | Allows authorized backend access | Web App | Amazon Cognito |
| TB3 | Triggers Lambda securely | API Gateway | Lambda |  
| TB4 | Enables responsible AI check and PII redaction without exposure | Lambda | Amazon Bedrock Guardrail |
| TB5 | Allows secure document retrieval | Lambda | OpenSearch Serverless |
| TB6 | Provides secure inference endpoint | Lambda | Amazon Bedrock |

#### Possible threat sources:

The table below categorizes the various threat sources mentioned across the threat statements in the next section:

| Category | Description | Examples |
|-|-|-|
| Legitimate Users | Valid users who unintentionally trigger issues | An internal actor, An end user|   
| Malicious Internal Actors | Trusted insiders who intentionally cause harm | An overprivileged LLM plugin, An internal plugin or agent developer, An LLM developer or trainer|  
| External Threat Actors | External attackers targeting the system | A threat actor, An external threat actor - A malicious user (with system access)|
| Untrusted Data Suppliers | External data sources that provide bad data | A third-party data supplier, A data supplier|  
| Unauthorized External Users | External entities with no system access | A malicious user (no system access)|
