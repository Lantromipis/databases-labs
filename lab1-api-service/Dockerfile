FROM maven:3.9.6-eclipse-temurin-21-jammy as maven-deps
RUN mkdir -p /usr/app

COPY pom.xml /usr/app/

RUN mvn -f /usr/app/pom.xml --batch-mode dependency:go-offline dependency:resolve-plugins


FROM maven:3.9.6-eclipse-temurin-21-jammy as build
COPY --from=maven-deps /root/.m2 /root/.m2

RUN mkdir -p /usr/app

COPY src/ /usr/app/src
COPY pom.xml /usr/app/

RUN mvn -f /usr/app/pom.xml clean install

FROM eclipse-temurin:21.0.1_12-jdk-jammy

ENV LANGUAGE='en_US:en'

# We make four distinct layers so if there are application changes the library layers can be re-used
COPY --from=build /usr/app/target/quarkus-app/lib/ /deployments/lib/
COPY --from=build /usr/app/target/quarkus-app/*.jar /deployments/
COPY --from=build /usr/app/target/quarkus-app/app/ /deployments/app/
COPY --from=build /usr/app/target/quarkus-app/quarkus/ /deployments/quarkus/

USER root

ENV JAVA_OPTS="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager"
ENV JAVA_APP_JAR="/deployments/quarkus-run.jar"

ENTRYPOINT ["/bin/bash", "-c", "java ${JAVA_OPTS} ${JAVA_OPTS_APPEND} -jar ${JAVA_APP_JAR}"]

