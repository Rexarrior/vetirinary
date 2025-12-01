FROM nginx:1.25-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config as default.conf
# In production, this will be overwritten by mounted nginx.prod.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80



