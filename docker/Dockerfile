FROM debian:bookworm

# Enable contrib component for index files
RUN echo "deb http://deb.debian.org/debian bookworm contrib" > /etc/apt/sources.list.d/astroplate.list && \
    echo "deb http://security.debian.org/debian-security bookworm-security contrib" >> /etc/apt/sources.list.d/astroplate.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates contrib" >> /etc/apt/sources.list.d/astroplate.list

# Copy the list of APT packages
COPY requirements/apt-requirements.txt /tmp/apt-requirements.txt

# Install system dependencies including contrib
RUN apt-get update && \
    xargs -a /tmp/apt-requirements.txt apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare Python environment
COPY requirements/python-requirements.txt /app/
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r /app/python-requirements.txt

# Copy project files
WORKDIR /app
COPY scripts/ /app/scripts/
COPY config/ /app/config/
COPY docker/entrypoint.sh /entrypoint.sh
COPY README.md README.md /app/

# Determine required index packages and install them
RUN python3 /app/scripts/index_file_helper.py > /tmp/index_packages.sh && \
    export APT_INDEX_PACKAGES=$(grep ^APT_INDEX_PACKAGES /tmp/index_packages.sh | cut -d= -f2 | tr -d '"') && \
    apt-get update && \
    apt-get install -y astrometry.net $APT_INDEX_PACKAGES && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set default index path
RUN echo "add_path /usr/share/astrometry" > /etc/astrometry.cfg && \
    echo "autoindex" >> /etc/astrometry.cfg

# Set entrypoint
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["scripts/annotate_constellations.sh"]
