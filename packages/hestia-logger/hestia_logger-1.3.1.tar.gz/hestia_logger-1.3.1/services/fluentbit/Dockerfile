# Use a slim Debian base for shell and package management
FROM debian:bullseye-slim

# Add Fluent Bit repository and install Fluent Bit + debugging tools
RUN apt-get update && \
    apt-get install -y \
        curl \
        bash \
        coreutils \
        gnupg2 && \
    curl https://packages.fluentbit.io/fluentbit.key | apt-key add - && \
    echo "deb https://packages.fluentbit.io/debian/buster buster main" > /etc/apt/sources.list.d/fluentbit.list && \
    apt-get update && \
    apt-get install -y fluent-bit=2.2.2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Fluent Bit configuration and Parser from the build context (services/fluentbit/)
COPY fluent-bit.conf /etc/fluent-bit/fluent-bit.conf
COPY parsers.conf /etc/fluent-bit/parsers.conf

# Ensure log directory exists and is writable
RUN mkdir -p /var/logs/hestia && chmod -R 777 /var/logs/hestia

# Set Fluent Bit binary path
ENV PATH="/opt/fluent-bit/bin:${PATH}"

# Default command
CMD ["fluent-bit", "-c", "/etc/fluent-bit/fluent-bit.conf"]