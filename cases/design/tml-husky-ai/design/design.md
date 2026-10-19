# husky-ai

Husky AI — A machine learning system to classify Huskies vs dogs. HuskyAI is a machine learning system designed to classify images and distinguish between huskies and non-huskies. It integrates secure data handling practices with a robust convolutional neural network (CNN) for image recognition. Secure Image Retrieval: HuskyAI uses TLS to securely fetch images from Azure Cognitive Services, ensuring encryption during data transmission and validating the server's authenticity to prevent man-in-the-middle attacks. Data Storage and Access Controls: Azure Blob Storage is used to store datasets, with public access fully blocked. Access is controlled using Role-Based Access Control (rbac) and Attribute-Based Access Control (ABAC) to enforce granular, identity-based permissions. Jupyter Notebooks, which host model development and experimentation, are also secured with rbac and ABAC, preventing unauthorized public access. Developer Authentication: Developers access the system through SSH keys protected by passphrases. This adds an additional layer of security, reducing the likelihood of unauthorized access even if keys are exposed. Model and Dataset Dataset Composition: The dataset comprises approximately 1,300 husky images and 3,000 non-husky images sourced via Bing's image search. Data undergoes manual cleansing and is split into training and validation sets to enhance model performance. Model Design: HuskyAI employs a CNN with: Convolutional layers for feature extraction. Max-pooling layers for dimensionality reduction. Dropout layers to prevent overfitting. Dense layers for final classification. The model is trained with the Adam optimizer and a learning rate of 0.0005, optimized for accuracy and computational efficiency. Security Considerations rbac and ABAC controls across storage and development environments ensure sensitive data and configurations are protected. TLS ensures secure communication channels, preventing eavesdropping or data interception during image retrieval. Applications HuskyAI is tailored for accurate image classification and can be adapted for other domains requiring precise visual differentiation, with a focus on maintaining strong security postures. HuskyAI combines state-of-the-art machine learning techniques with stringent security controls, including secure communications, robust access management, and encrypted developer authentication, to deliver a reliable and secure image classification system. A machine learning system to classify Huskies vs dogs

## Components
- Simple Python Web Server
- API Gateway
- Bastion Server
- Gather Images Application - Python
- Jupyter Notebook
- Deployment Service
- Training And Validation Images Storage Blob
- API Key Storage
- Authorized Keys Storage
- Machine Learning Model Storage Blob
- Source Code And Configuration Storage
- Bastion Logs Storage
- Azure Cache for Redis

## Data flows
- azure-cognitive-services → gather-images
- third-party-tools → gather-images
- third-party-tools → jupyter
- engineer → gather-images
- engineer → jupyter
- gather-images → training-images-blob
- api-key-storage → gather-images
- training-images-blob → jupyter
- gather-images → jupyter
- jupyter → ml-models-blob
- ml-models-blob → deployment-service
- source-code-config-storage → deployment-service
- user → api-gateway
- bastion → api-gateway
- api-gateway → web-service
- bastion → web-service
- ml-models-blob → web-service
- deployment-service → bastion
- bastion → bastion-logs-storage
- infrastructure-admin → bastion
- bastion → ml-models-blob
- secret-key-storage → bastion
- third-party-tools → web-service

## Trust zones
- Production Trust Zone
- Experimental Trust Zone
- Public Internet