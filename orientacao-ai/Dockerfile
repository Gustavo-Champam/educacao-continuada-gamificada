FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /src
COPY pom.xml .
COPY src src
RUN mvn -B verify
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /src/target/orientacao-ai-0.0.1-SNAPSHOT.jar app.jar
ENTRYPOINT ["java","-jar","app.jar"]
