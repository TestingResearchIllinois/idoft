# Use a Maven image with a configurable Java version
ARG JAVA_VERSION=17
FROM maven:3.9.4-eclipse-temurin-${JAVA_VERSION}

WORKDIR /app

RUN apt-get update && apt-get install -y git && apt-get clean

# Thanks - https://github.com/TestingResearchIllinois/idoft/pull/1491
ENV MAVEN_OPTS="-XX:+TieredCompilation -XX:TieredStopAtLevel=1"

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

