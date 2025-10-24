# The Connected Data Knowledge Graph Challenge

![CDKG](https://github.com/user-attachments/assets/e24e7615-df1e-4dc7-a527-abc274c2a341)



**Let’s build a curated Knowledge Graph based on the collective wisdom of 260+ experts**

  

The [Connected Data](https://connecteddataworld.com) platform provides a Community, Events, and Thought Leadership for those who use the Relationships, Meaning and Context in Data to achieve great things.

  

​We've been Connecting Data, People & Ideas since 2016. We focus on Knowledge Graphs, Graph Analytics / AI / Databases / Data Science and Semantic Technology.

  

Over the years, we have organized numerous events big and small, with our [flagship London conference](https://www.connected-data.london/) attracting thousands of attendees.

  

We have had the honor of hosting luminaries such as Gary Marcus, Gadi Singer, Kirell Benzi and Sir Nigel Shadbolt, as well as emerging speakers who went on to achieve great things.

  

​We are happy to have helped pave the way for the widespread recognition these technologies are receiving today alongside our community.

  

The collective knowledge of the leaders and innovators who have honored us with their presence is vast. Publicly available, but untapped.

  

This is why we launched the [Connected Data Knowledge Graph Challenge](https://github.com/Connected-Data/cdkg-challenge). 

  

The goal is to make our collective knowledge easy to discover, explore, digest, combine and reuse.

  

To do that, we combine our greatest strengths: community, knowledge, and technology.

## The Connected Data Knowledge Graph
This what is included in the first release of the CDKG:

- `[Domain Metamodel](https://github.com/Connected-Data/cdkg-challenge/blob/main/Data%20Model/README.md)`: Technology agnostic, simple graph of entities and relationships
- `Property Graph Schema`: Domain graph and Lexical graph
- `Metadata`: Speakers and Sessions 
- `Raw data`: Session transcripts 
- `Knowledge Graph`: Data on Categories, Events, Speakers, Talks, Tags and their relationships
- `Evaluation data`: Baseline questions and answers on the data included in the CDKG 
- `Source code`: Code used to construct and query the Knowledge Graph using Kuzu.


## The Problem

- There are 150+ expert and practical talks on Knowledge Graphs, Graph AI / Analytics / Data Science and Semantic Technology from previous [Connected Data Conferences on YouTube](https://www.youtube.com/@ConnectedData).
    
- People have little time to watch videos to learn and gather knowledge from experts and don’t know how to find the right videos. Thus, they miss opportunities to turn these great insights and best practices into something valuable.
    

## What we are doing about it

Recently, [we started experimenting](https://www.linkedin.com/feed/update/urn:li:activity:7214552580541059072/) with tools and a workflow that would enable easier access to this treasure trove of collective knowledge.

  

We used one of our videos as a testbed. More specifically, we used our [Connected Data London Ask Me Anything Roundtable from July 2024](https://www.youtube.com/watch?v=EsDzpptLKd8). This online roundtable featured 10 experts and it was a deep dive in Connected Data. 

  

We took the following steps:

1. Extracted and enhanced the transcript using an off-the-shelf tool
    
2. Generated a Knowledge Graph based on the transcript using an LLM-powered tool.
    
3. Used the built-in UI to explore the generated Knowledge Graph and tweaked auto-generated queries and visualization to produce something representative of the conversation.
    

  

This 60-minute experiment already taught us a few things about both the potential and the shortcomings of the approach.

![image](https://github.com/user-attachments/assets/d59667dd-5b76-4688-bda1-c80faa120ba5)


Focusing on the Knowledge Graph creation, which is the most interesting part: it was a good starting point and certainly impressive compared to what was the state of the art previously. Still, the process was not flawless and the outcome should not be blindly trusted. 

  

- The quality of the input matters, hence processing the transcript before using it as input to generate a Knowledge Graph was necessary.
    
- There was both redundancy and missing entities and relationships in the auto-generated Knowledge Graph. 
    
- Domain expertise, technical knowledge and manual labor are required for a production-ready outcome. 
    

  

## Our vision

Based on this learning experience and the very positive feedback it generated, we are embarking on the next steps in this journey.

  

We are calling the community to work with us on building the Connected Data Knowledge Graph.

  

The Connected Data Knowledge Graph will act as a gateway to the collective wisdom 260+ experts have contributed to the Connected Data platform since 2016.

  

This curated Knowledge Graph will make it easier to discover, explore, digest, combine and reuse our collective knowledge.

  

We envision making the Connected Data Knowledge Graph available for querying and exploration.

  

We would also like to use the Connected Data Knowledge Graph to power downstream applications.

## The Connected Data Knowledge Graph Challenge

<img width="790" alt="CDKG_Logo" src="https://github.com/user-attachments/assets/fc8a4038-c8c9-4f42-8168-179850f5239e">

We at Connected Data are launching the Connected Data Knowledge Graph Challenge as an open source project. 
  

The goal is to build the Connected Data Knowledge Graph based on the Connected Data treasure trove and make it available under a permissive open source license.
  

Here is what we are offering:

1. Access to Connected Data content
    
2. Access to a wide range of tools
    
3. Guidance and expertise in 
    1. Content processing
    2. Pipeline assembly
    3. Knowledge graph modeling
    4. Infrastructure setup
    5. Application development
    6. Open source project management
    5. Exposure and awareness building
    

Here is the process we are looking to initiate:

1. Generating transcripts from Connected Data videos and podcasts
    
2. Processing auto-generated transcripts to add metadata and improve accuracy
    
3. Using the transcripts to create a Knowledge Graph
    
4. Consolidating and editing the Knowledge Graph
    
5. Enabling public access to the Knowledge Graph
    
 

We will be looking for solutions that enable us to make the Knowledge Graph accessible by:

6. Offering a visualization layer for the Knowledge Graph
    
7. Offering a natural language interface for the Knowledge Graph
    

## How you can can help

  

We can use all the help we can get for the Connected Data Knowledge Graph Challenge. 

  

Calling out Connected Data enthusiasts, seasoned professionals and solution providers.

  

- The team will be led by George Anadiotis and Prashanth Rao. 
    
- Work in progress will be organized via an [open source repository](https://github.com/Connected-Data/cdkg-challenge).
    
- Outcomes will be made available as they are generated, and presented in a session in the upcoming [Connected Data London 2024 conference](https://www.connected-data.london/).
    

### Connected Data enthusiasts: Volunteer

We are building a small team of volunteers to help with steps 1 to 3 in the process: Generating and processing transcripts and using them to create a Knowledge Graph.


Are you able to help with any of these tasks?

- Content curation
    
- Data processing
    
- Pipeline setup
    
- API calls
    
- Graph tool setup and operation
      

Then click [here](https://www.connected-data.london/contact-us) to join our team of volunteers, or simply browse the [open source repository](https://github.com/Connected-Data/cdkg-challenge) and see if there are open tasks available.


### Connected Data professionals: Consult

Seasoned Connected Data professionals are invited to help with steps 3 - 5 in the process: Using the transcripts to create a Knowledge Graph, consolidating, editing and enabling public access to the Knowledge Graph.

Are you able to help with any of these tasks?

- Graph tool setup and operation
    
- Knowledge Graph modeling
    
- Graph store setup and fine tuning
    
- Software and data architecture
    
- Content, documentation and public speaking
  

Then click [here](https://www.connected-data.london/contact-us) to get in touch with George and Prashanth.

### Connected Data solution providers: Create

Connected Data solution providers are invited to help with steps 6 - 7 in the process: Offering a visualization layer and a natural language interface for the Knowledge Graph.

Are you able to offer easy to set up and configure, publicly accessible solutions for the following at no or low cost?

- Infrastructure to host the Knowledge Graph
    
- Tooling to visualize the Knowledge Graph
    
- Tooling to query the Knowledge Graph using natural language
    

Then simply browse our [open source repository](https://github.com/Connected-Data/cdkg-challenge), or get in touch with George and Prashanth. Solution provider contributions for this role will be developed 
