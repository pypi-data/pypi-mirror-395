# Traefik Certificates Directory

Place your SSL certificates here:

- `cert.pem` - Your SSL certificate (public key)
- `key.pem` - Your SSL private key

## Example with Let's Encrypt

```bash
# Copy your Let's Encrypt certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./key.pem
```

## Example with Self-Signed Certificate (for testing)

```bash
# Generate self-signed certificate (NOT for production)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout key.pem \
  -out cert.pem \
  -subj "/CN=localhost"
```

## Security Notes

⚠️ **NEVER commit these files to Git!**
- Add `*.pem` to `.gitignore`
- Use proper certificate management in production
- Rotate certificates before expiration
