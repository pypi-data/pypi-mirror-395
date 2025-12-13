# Evaluate - Quick Start Docker Container

This Quick Start guide assumes you know why you want to run evaluate, that your GitLab version is 16.x or newer, and what your goals are.

## Setting up the Evaluate Docker Container

Choose a host to run the docker container on, **NOT** the Gitlab instance itself, preferably "close" to the Source GitLab infrastructure.

```bash
# Pull the docker container
docker pull registry.gitlab.com/gitlab-org/professional-services-automation/tools/utilities/evaluate:latest
```

Providing 2 different ways here to spin up the evaluate docker container.  The first way makes managing the reports a little easier.  Second way is if you can't map a docker data volume for some reason.

### Example with mapped data volume

```bash
# Spin up container WITH a data volume (Suggested for ease)
# Easiest for getting reports out of the container and into somewhere useable.
# Assumes you are running as root with a directory of /root/evaluate.
# Change </root/evaluate> to appropriate user directory if not root.

docker run --name evaluate -v </root/evaluate>/data:/opt/evaluate -it registry.gitlab.com/gitlab-org/professional-services-automation/tools/utilities/evaluate:latest /bin/bash
```

### Example without mapped data volume

```bash
# Spin up container without mapping a data volume (If docker mapped volumes aren't realistic)
docker run --name evaluate -it registry.gitlab.com/gitlab-org/professional-services-automation/tools/utilities/evaluate:latest /bin/bash
```

## Running Evaluate

Depending on the size of your instance and arguments supplied to evaluate, it can take a long time to run.  Warning or Error Messages might appear in the logs, do not worry about these **unless** the run fails and crashes out.
Run these commands from the Evaluate Container. If you aren't currently in the container and you followed the previous commands, use `docker exec -it evaluate /bin/bash` to reattach to a running container.

### Basic Example

Appropriate for GitLab Self Managed

```bash
evaluate-gitlab -t <access-token-with-api-scope> -s https://gitlab.example.com
```

### Group Targeted Example

If the above is taking too long on GiLab Self Managed, or you are running Evaluate against gitlab.com, or you encounter errors with the [Basic Example](#basic-example), consider limiting Evaluate to a group and its sub-groups. In this example we are targeting group `42`.

```bash
evaluate-gitlab -t <access-token-with-api-scope> -s https://gitlab.example.com -g <Group ID, i.e. 42>
```

### SSL problems or Self-Signed certs

If you are getting SSL errors or know you have self-signed certs, use `-i` argument to ignore SSL verification errors.

```bash
evaluate-gitlab -t <access-token-with-api-scope> -i -s https://gitlab.example.com -g <Group ID, i.e. 42>
```

## Getting the Report

After Evaluate finishes running, you will want to review the output.  Depending on how you setup your container, there are a few ways to do this.

### Evaluate Container with Mapped Data Volumes

From your workstation use your favorite SCP tool, example assumes a terminal (Mac or Linux).

```bash
# Change <root/evaluate> to your host user if it wasn't root
# Downloads the evaluate_report.xlsx to the current directory on your workstation
# Open with your normal workstation File Management
scp <hostname>:<root/evaluate>/evaluate_report.xlsx ./evaluate_report.xlsx
```

### Evaluate Container without Mapped Data Volumes

From the docker host, use `docker cp` to get the report from container to host

```bash
# Copies the report from the container to the host's current directory
docker cp evaluate:/opt/evaluate/evaluate_report.xlsx .
```

From your workstation use your favorite SCP tool, example assumes a terminal (Mac or Linux).

```bash
# Change <root/evaluate> to where you `docker cp'd` the report to in the previous step
# Downloads the evaluate_report.xlsx to the current directory on your workstation
# Open with your normal workstation File Management
scp <hostname>:<root/evaluate>/evaluate_report.xlsx ./evaluate_report.xlsx
```

### Understanding the output

The XLSX Report has instructions at the top, but there is also a more extensive guide [here](../../reading-the-output.md). 