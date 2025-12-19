# Demo Video Script (2 Minutes)

This script is designed to help you record a compelling demo of IDP-Lite.

## Scene 1: Introduction (0:00 - 0:20)
*Visual: IDP-Lite README or Title Slide*
"Hi, I'm [Name]. I built IDP-Lite to demonstrate how platform engineering can reduce operational burden. Let me show you how we can go from zero to a deployed service in under 2 minutes."

## Scene 2: Service Creation (0:20 - 0:50)
*Visual: Terminal / VS Code*
"First, I'll use the CLI to generate a new Spring Boot service."
`python -m platform.cli.idp create service payment-service --template springboot_service --ai-enhance`
"Notice I used the `--ai-enhance` flag. The platform not only scaffolds the code but provides structural optimizations."
*Show generated files and the `AI_OPTIMIZATION.md` report.*

## Scene 3: Developer Experience (0:50 - 1:20)
*Visual: VS Code showing `GreetingsController.java` and `pom.xml`*
"The service comes with health checks, metrics, and standard logging pre-configured. No copy-pasting from StackOverflow. It's ready for production out of the box."

## Scene 4: Verify & Deploy (1:20 - 1:45)
*Visual: Terminal*
"I can build it immediately."
`(If Java installed) ./mvnw clean package`
"And deploy it locally with the platform's standard docker compose profiles."
`cd examples/payment-service && docker compose up`

## Scene 5: Scalability & Conclusion (1:45 - 2:00)
*Visual: `docs/multi_cloud.md` or Architecture Diagram*
"This specific implementation supports AWS, Azure, and Google Cloud deployment patterns. IDP-Lite proves that with the right abstractions, we can enable velocity without sacrificing control. Thanks for watching."
