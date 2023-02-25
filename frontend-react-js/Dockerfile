FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js

WORKDIR /frontend-react-js

RUN npm install

HEALTHCHECK --interval=12s --timeout=12s --start-period=30s \
    CMD node healthcheck.js

EXPOSE ${PORT}
