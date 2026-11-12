# Serves the ready-built site in dist/ with nginx.
# Rebuild dist/ with `python build.py` and push before deploying.
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY dist/ /usr/share/nginx/html/
EXPOSE 80
