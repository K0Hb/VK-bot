FROM python

ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY pyproject.toml ./

RUN python -m pip install pip wheel setuptools --upgrade

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY .  /bot

EXPOSE 8000

CMD ["make", "runbot"]