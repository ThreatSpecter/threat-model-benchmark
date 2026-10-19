# Threat composer

**Motivation for externalizing this threat model:** `We've included this example threat model to support a training workshop to instruct participants on how you can use Threat Composer to perform feature-based threat modeling. We have chosen the threat composer tool itself as an example to illustrate this, along with a hypothetical feature enhancement to Threat Composer. This threat model does not claim to be 100% complete for every possible interaction, and is purposefully incomplete in some areas so as to aid our training workshop learning outcomes. The example threat model aims to give the reader an example of what a set of threats, assumptions and mitigations could look like. We've chosen to share this example as it provides a common reference point for people who are starting off with Threat composer. You may have different perspectives on the assumptions, threats and mitigations. This is ok, and could be used to start conversations in your organization within the context of your risk appetite. You are responsible for making your own independent assessment of this threat model and its applicability to your organization.`

## Goal

A simple threat modeling tool to help humans to reduce time-to-value when threat modeling

## Summary

The process of [threat modeling](https://catalog.workshops.aws/threatmodel/en-US/introduction) helps you identify security issues and develop a strategy to address them in the _context_ of your system.  A threat model directly supports your ability to define, agree upon, and communicate what is necessary in order to deliver a secure product or service. You can threat model very early in your design phase. These early insights put you in a better position to identify sensible design choices early in the cycle, and efficiently build and ship your workload securely. Identifying and fixing security issues at design time is exponentially easier to do than doing so once the workload has been built.

There are many ways to perform threat modeling. Much like programming languages, there are advantages and disadvantages to each. You should choose the approach that works for you, and communicate it within your organization. A good place to start is [Shostack’s 4 Question Frame for Threat Modeling](https://github.com/adamshostack/4QuestionFrame) which proposes four simple open ended questions.

The Threat composer tool has been built for the following reasons:

1. **Coming up with useful threats is often tougher than coming up with mitigations**. Feedback from builders regarding the "What can go wrong?" question is that there are two key challenges in this step - firstly, no generally agreed standard on what 'good' looks like. This is contextual based on the system being assessed and the ownership model of the teams involved; and, secondly, there is no canonical list of possible things that could go wrong. Hence, threat identification necessitates brainstorming and collaboration between the individuals involved in the threat modeling process, and often involves starting from a "blank page". Threat composer provides a prescriptive threat articulation structure, this helps users create threat statements with less effort. The tool supports starting from any part of the threat statement, and encourages the user to be more complete and descriptive to help ensure the threat statement allows for both for prioritization for mitigation and sufficient information to devise mitigation strategies. In addition, the Threat Composer tool aims to aid the brainstorming and collaboration process by including full threat statement examples and per field examples which a customer can use as inspiration or as a starting point for their own custom and contextual threat statements.
2. **Improve quality and coverage.** One of the toughest questions to answer is “did we do a good enough job?” because it can be highly subjective. Threat composer includes an ‘insights dashboard’ to help you quickly answer some of the easier questions, including (a) threats without linked mitigations, (b) unprioritized threats, (c) threat category distribution, and (d) based on threat grammar usage, potential improvement to inputs for mitigation or prioritisation.
3. **Threat modeling is non-linear.** The theory of threat modeling is often taught as a linear process, where a person or team works on each of the threat modeling questions separately. However, in practice ones thoughts and conversations naturally flow from one to the other in a non-linear fashion. For example, it’s often the case that you may think of a mitigation (“what are we going to do about?”) immediately after you’ve thought of a threat (“what can go wrong?). Threat composer aims to support this kind of non-linear and natural workflow.
4. **Threat modeling is iterative.** The process is iterative both at a micro and at the macro level. For example, at a micro level, you may iterate on a given threat to the point you find you could [decompose](https://catalog.workshops.aws/threatmodel/en-US/what-can-go-wrong/threat-grammar/decomposition) it into two discrete threats. At a macro level, a threat model can (and should) evolve and mature as the thing you are threat modeling evolves through the software/hardware development lifecycle. In the early stages of design you may need to make a lot of [assumptions](https://catalog.workshops.aws/threatmodel/en-US/what-are-we-working-on/exercise/state-your-assumptions), and as time passes previous assumptions may become [invalidated](https://catalog.workshops.aws/threatmodel/en-US/introduction/when-to-threat-model). As new design decisions are made, new threats are thought of and mitigations go from being planned to being implemented. Threat composer has been designed to support this iterative design and development lifecycle, and to support the ability of having a “living” threat model-as-code as your feature or service evolves and matures.

## Features (existing)

- Capture and store systems description, architecture diagram, and dataflow diagram.
- Capture and store assumptions related to the systems design, threats and/or mitigations, along with mapping of assumptions to threats to mitigations.
- Help iteratively compose useful threats, and encourage brainstorming. This feature is also available via a dedicated [‘Threats Only’](https://awslabs.github.io/threat-composer?mode=ThreatsOnly) mode.
  - Rendering structured threat statements (aligned to a prescriptive threat grammar) based on user input.
  - Supporting an adaptive threat statement structure, this helps create progressively more complete threats.
  - Provide dynamic suggestions based on supplied and missing user input.
  - Provide complete threat statement examples to aid contextual brainstorming.
- Capture and store mitigation candidates and mapping to threats.
- Create a threat model document based on user-supplied input.
- Help users answer "Did we do a good enough job" by providing insights and suggestions for bar-raising actions via an 'Insights dashboard'
- JSON import/export capabilities to enable persistent storage, sharing, and version control outside of the web browser (e.g. by using git).
- Markdown and PDF static downloads of the threat model document.
- Workspace separation to allow working on multiple threat models.
- By default, data persisted only client-side within the browser (100% local storage).

## Features (new - hypothetical)

- (new feature proposed as an example for re:Inforce 2024 workshop) Centrally save and retrieve project workspaces for users that have their own deployment of Threat Composer

## Architecture

This threat model covers the self-hosted version of Threat Composer:

1. **Self-hosted** - Deploying to their AWS account using the included AWS CDK app. Either:
   - **Static Website Only** - The application CloudFormation stack include a CloudFront distribution, S3 website bucket, and an associated AWS WAF WebACL.
   - **Static Website with CI/CD** - The CI/CD infrastructure includes a CodeCommit repository and a CodePipeline. The CodePipeline deploys the application stack (CloudFront distribution + S3 website bucket + AWS WAF WebACL) into the nominated dev and prod environments.

**Notes:**

- All user-supplied input is stored in browser storage, there is no backend nor any dynamic API calls for the base version of Threat Composer, and this feature-driven threat model workshop covers a hypothetical new feature to include a backend

### Customer messaging and guidance

Customer guidance for the base Threat Composer setup is published at the [README.md](https://github.com/awslabs/threat-composer#readme) file on the GitHub repository for this tool.

The guidance will cover: Features, Usage, Security considerations, Deployment options and instructions, Development and contribution, License and References to resourcing on how to threat model.

## APIs (new - hypothetical )

(new APIs proposed as an example for re:Inforce 2024 workshop)

### ListWorkspaces

##### Request Parameters

none

#####

##### Response Elements

| parameter name   | data type        |
| ---------------- | ---------------- |
| threatModelId    | (STRING - UUID4) |
| threatModelTitle | (STRING)         |

### UploadWorkspace

##### Request Parameters

| parameter name   | data type        |
| ---------------- | ---------------- |
| threatModelId    | (STRING - UUID4) |
| threatModelTitle | (STRING)         |
| authorId         | (STRING - UUID4) |
| projectId        | (STRING - UUID4) |

#####

##### Response Elements

| parameter name      | data type        |
| ------------------- | ---------------- |
| threatModelId       | (STRING - UUID4) |
| threatModelUploaded | (BOOLEAN)        |

### RemoveWorkspace

##### Request Parameters

| parameter name | data type        |
| -------------- | ---------------- |
| threatModelId  | (STRING - UUID4) |

#####

##### Response Elements

| parameter name      | data type        |
| ------------------- | ---------------- |
| threatModelId       | (STRING - UUID4) |
| threatModelUploaded | (BOOLEAN)        |

### DescribeWorkspace

##### Request Parameters

| parameter name | data type        |
| -------------- | ---------------- |
| threatModelId  | (STRING - UUID4) |

#####

##### Response Elements

| parameter name         | data type        |
| ---------------------- | ---------------- |
| threatModelId          | (STRING - UUID4) |
| threatModelUploaded    | (BOOLEAN)        |
| threatModelVersion     | (INT)            |
| threatModelLastUpdated | (DATE)           |
| authorId               | (STRING - UUID4) |
| projectId              | (STRING - UUID4) |

## Data flow

### Self Deployed

#### WebApp content

- A1 - User device browser `/GET` to Amazon CloudFront hosted endpoint
- A2 - CloudFront requests assets from Amazon S3 Origin (if not in cache)
- A3 - S3 Origin responds with assets (Assets: `Static assets`)
- A4 - CloudFront responds to the client request passing the static assets (Assets: `Static assets`)

#### User authentication

- A5 - User provides credential details to the Amazon Cognito
- A6 - Amazon Cognito returns an auth token for successfully authenticated logins

#### Centralized storage and retrieval

- A7 - Client-side app calls API Gateway endpoint to list, upload, remove or describe a project workspace
- A8 - API Gateway calls a Lambda function to perform the associated business logic behind the authenticated user request
- A9 - Lambda function interacts with DynamoDB to store, retrieve, remove, or update the associated project workspace JSON and project metadata

### APIs

- ListProjectWorkspaces
- UploadProjectWorkspace
- RemoveProjectWorkspace
- DescribeProjectWorkspace

### Assets

- **User-supplied assets (i.e. input)** - application description, architecture description and diagram, data flow description and diagram, threat statements, mitigation candidates, assumptions, impacted assets, mapping between threats, mitigations and assets
- **User credentials** - Login credentials to authenticate to Amazon Cognito
- **Tool static assets** - Example threat statements, Redact client side web application and Typescript CDK project
