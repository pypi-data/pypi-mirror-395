#  Copyright (c) 2025 The Eclipse Foundation
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0.
#
#  SPDX-License-Identifier: EPL-2.0
#
#  Contributors:
#      asgomes - Initial definition

ARG JAVA_VERSION="21"
ARG MAVEN_VERSION="3.9.9"
ARG PYTHON_VERSION="3.13.5"

FROM eclipse-temurin:${JAVA_VERSION}-jdk-alpine AS java
FROM maven:${MAVEN_VERSION}-eclipse-temurin-${JAVA_VERSION} AS maven
FROM python:${PYTHON_VERSION}-alpine3.20

LABEL maintainer="André Gomes <andre.gomes@eclipse-foundation.org>"
LABEL description="Docker image for Eclipse IP Analysis"
LABEL version="0.1.0"

ENV JAVA_HOME=/opt/java/openjdk
ENV MAVEN_HOME=/usr/share/maven
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Java and Maven
COPY --from=java /opt/java/openjdk ${JAVA_HOME}
COPY --from=maven /usr/share/maven ${MAVEN_HOME}
COPY --from=maven /usr/local/bin/mvn-entrypoint.sh /usr/local/bin/mvn-entrypoint.sh
COPY --from=maven /usr/share/maven/ref/settings-docker.xml /usr/share/maven/ref/settings-docker.xml
RUN ln -s ${MAVEN_HOME}/bin/mvn /usr/bin/mvn

# Install Git
RUN apk update && apk add --no-cache git \
    && rm -rf /var/cache/apk/*

# Install Eclipse IPA
RUN pip install --no-cache-dir eclipse-ipa

WORKDIR /app

# Default command
CMD ["eclipse-ipa", "--help"]
