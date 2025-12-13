# 🌐 RAFAEL Domain Configuration

**Primary Domain**: rafaelabs.xyz  
**Status**: REGISTERED ✅  
**Date**: December 7, 2025

---

## 🎯 Domain Information

### Primary Domain
- **Domain**: rafaelabs.xyz
- **Registrar**: Namecheap (recommended)
- **Cost**: $10-15/year (.xyz TLD)
- **Status**: REGISTERED
- **Renewal**: Annual

### Why rafaelabs.xyz?
- ✅ **Professional**: "labs" indicates research/innovation
- ✅ **Memorable**: Short and easy to remember
- ✅ **Tech-focused**: .xyz is popular in tech community
- ✅ **Affordable**: ~$10-15/year vs $50-100 for .ai
- ✅ **Available**: Secured for RAFAEL Framework

---

## 🏗️ Complete Architecture

### Production URLs

```
rafaelabs.xyz (Main Domain)
├── https://rafaelabs.xyz
│   └── Landing page & marketing site
│
├── https://dashboard.rafaelabs.xyz
│   └── Web Dashboard (Flask app)
│
├── https://api.rafaelabs.xyz
│   └── REST API endpoints
│
├── https://docs.rafaelabs.xyz
│   └── Documentation site
│
├── https://beta.rafaelabs.xyz
│   └── Beta program landing page
│
└── https://demo.rafaelabs.xyz
    └── Live demo environment
```

---

## 📧 Email Configuration

### Email Addresses

#### Primary Contacts
- **info@rafaelabs.xyz** - General inquiries
- **support@rafaelabs.xyz** - Technical support
- **hello@rafaelabs.xyz** - Friendly contact

#### Program Specific
- **beta@rafaelabs.xyz** - Beta program applications
- **dev@rafaelabs.xyz** - Developer relations
- **security@rafaelabs.xyz** - Security reports

#### Team (Future)
- **team@rafaelabs.xyz** - Team communications
- **careers@rafaelabs.xyz** - Job applications
- **press@rafaelabs.xyz** - Media inquiries

### Email Provider Options

#### Option 1: Google Workspace (Recommended)
- **Cost**: $6/user/month
- **Features**: Gmail interface, 30GB storage, Calendar, Drive
- **Setup**: workspace.google.com
- **Professional**: Full Google suite

#### Option 2: Zoho Mail
- **Cost**: FREE (up to 5 users)
- **Features**: 5GB storage, webmail
- **Setup**: zoho.com/mail
- **Budget-friendly**: Good for starting

#### Option 3: ProtonMail
- **Cost**: $5/user/month
- **Features**: Encrypted email, privacy-focused
- **Setup**: proton.me
- **Security-focused**: End-to-end encryption

---

## 🚀 DNS Configuration

### Cloudflare Setup (Recommended)

#### Nameservers
```
Update at registrar (Namecheap):
ns1.cloudflare.com
ns2.cloudflare.com
```

#### DNS Records

```
Type    Name        Content                         TTL     Proxy
A       @           [Vercel IP]                    Auto    Yes
A       www         [Vercel IP]                    Auto    Yes
CNAME   dashboard   rafael-dashboard.railway.app   Auto    Yes
CNAME   api         rafael-api.railway.app         Auto    Yes
CNAME   docs        rafael.readthedocs.io          Auto    No
CNAME   beta        rafael-beta.vercel.app         Auto    Yes
CNAME   demo        [DigitalOcean IP]              Auto    Yes
```

#### MX Records (for email)
```
Type    Name    Content                 Priority    TTL
MX      @       mx1.zoho.com           10          Auto
MX      @       mx2.zoho.com           20          Auto
MX      @       mx3.zoho.com           50          Auto
```

#### TXT Records (for verification)
```
Type    Name    Content                             TTL
TXT     @       "v=spf1 include:zoho.com ~all"     Auto
TXT     @       "google-site-verification=..."     Auto
```

---

## 🔒 SSL/TLS Configuration

### Cloudflare SSL
- **Mode**: Full (strict)
- **Always Use HTTPS**: Enabled
- **Automatic HTTPS Rewrites**: Enabled
- **Minimum TLS Version**: 1.2
- **TLS 1.3**: Enabled

### Let's Encrypt (for direct hosting)
```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d rafaelabs.xyz -d www.rafaelabs.xyz

# Auto-renewal
sudo certbot renew --dry-run
```

---

## 🎨 Subdomain Details

### 1. Main Site (rafaelabs.xyz)
- **Purpose**: Landing page, marketing, documentation
- **Technology**: Static site (Next.js/React)
- **Hosting**: Vercel (FREE)
- **Features**: 
  - Hero section
  - Feature showcase
  - Use cases
  - Pricing
  - Blog
  - Contact form

### 2. Dashboard (dashboard.rafaelabs.xyz)
- **Purpose**: Web-based monitoring and control
- **Technology**: Flask + TailwindCSS
- **Hosting**: Railway ($5/month)
- **Features**:
  - Real-time monitoring
  - Module management
  - Chaos testing
  - Pattern library
  - Guardian approvals

### 3. API (api.rafaelabs.xyz)
- **Purpose**: REST API for integrations
- **Technology**: FastAPI or Flask
- **Hosting**: Railway ($5/month)
- **Endpoints**:
  - /api/status
  - /api/modules
  - /api/chaos/simulate
  - /api/vault/patterns
  - /api/guardian/approvals

### 4. Docs (docs.rafaelabs.xyz)
- **Purpose**: Technical documentation
- **Technology**: MkDocs or Sphinx
- **Hosting**: ReadTheDocs (FREE)
- **Content**:
  - Getting started
  - API reference
  - Architecture
  - Examples
  - FAQ

### 5. Beta (beta.rafaelabs.xyz)
- **Purpose**: Beta program landing page
- **Technology**: Static HTML/CSS/JS
- **Hosting**: Vercel (FREE)
- **Features**:
  - Program overview
  - Application form
  - Benefits
  - Timeline
  - FAQ

### 6. Demo (demo.rafaelabs.xyz)
- **Purpose**: Live interactive demo
- **Technology**: Docker container
- **Hosting**: DigitalOcean ($5/month)
- **Features**:
  - Interactive playground
  - Pre-configured examples
  - Real-time visualization
  - Code editor

---

## 💰 Cost Breakdown

### Annual Costs

| Item | Cost | Provider |
|------|------|----------|
| Domain (rafaelabs.xyz) | $10-15 | Namecheap |
| SSL Certificate | FREE | Let's Encrypt/Cloudflare |
| CDN/DNS | FREE | Cloudflare |
| Email (5 users) | FREE-$72 | Zoho/Google |
| **Subtotal (Domain)** | **$10-87/year** | |

### Monthly Hosting Costs

| Service | Cost | Provider |
|---------|------|----------|
| Landing Page | FREE | Vercel |
| Dashboard | $5 | Railway |
| API | $5 | Railway |
| Docs | FREE | ReadTheDocs |
| Beta Page | FREE | Vercel |
| Demo | $5 | DigitalOcean |
| **Subtotal (Hosting)** | **$15/month** | |

### Total Annual Cost
```
Domain: $10-15
Email: $0-72 (optional)
Hosting: $180 ($15/month × 12)
---
Total: $190-267/year
```

### Budget Options

#### Minimal ($10/year)
- Domain only
- Use free hosting (Vercel, Railway free tier)
- Use free email (Zoho)

#### Standard ($190/year)
- Domain + hosting
- Free email
- All services running

#### Professional ($267/year)
- Domain + hosting
- Google Workspace email
- Full professional setup

---

## 🚀 Deployment Guide

### Step 1: Domain Setup
```bash
# 1. Domain already registered at Namecheap
# 2. Login to Namecheap dashboard
# 3. Go to Domain List → rafaelabs.xyz → Manage
```

### Step 2: Cloudflare Setup
```bash
# 1. Create Cloudflare account
# 2. Add site: rafaelabs.xyz
# 3. Copy nameservers
# 4. Update nameservers at Namecheap
# 5. Wait for DNS propagation (24-48 hours)
```

### Step 3: Deploy Dashboard
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd dashboard
railway init
railway up

# Add custom domain in Railway dashboard
# dashboard.rafaelabs.xyz → Railway URL
```

### Step 4: Deploy Landing Page
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd landing
vercel --prod

# Add custom domain in Vercel dashboard
# rafaelabs.xyz → Vercel
# www.rafaelabs.xyz → Vercel
```

### Step 5: Setup Email
```bash
# Option 1: Zoho Mail (FREE)
1. Go to zoho.com/mail
2. Sign up for free plan
3. Add domain: rafaelabs.xyz
4. Verify domain (add TXT record)
5. Add MX records
6. Create email accounts

# Option 2: Google Workspace ($6/month)
1. Go to workspace.google.com
2. Start free trial
3. Add domain: rafaelabs.xyz
4. Verify domain
5. Add MX records
6. Create email accounts
```

### Step 6: Configure DNS
```bash
# In Cloudflare dashboard, add DNS records:

# Main site
A     @           [Vercel IP]        Auto    Proxied
A     www         [Vercel IP]        Auto    Proxied

# Services
CNAME dashboard   [Railway URL]      Auto    Proxied
CNAME api         [Railway URL]      Auto    Proxied
CNAME docs        [ReadTheDocs]      Auto    DNS only
CNAME beta        [Vercel URL]       Auto    Proxied
CNAME demo        [DigitalOcean IP]  Auto    Proxied

# Email
MX    @           mx1.zoho.com       10      Auto
MX    @           mx2.zoho.com       20      Auto

# Verification
TXT   @           "v=spf1 include:zoho.com ~all"
```

---

## ✅ Verification Checklist

### Domain
- [x] Domain registered (rafaelabs.xyz)
- [ ] Nameservers updated to Cloudflare
- [ ] DNS propagated (check: whatsmydns.net)
- [ ] SSL certificate active
- [ ] HTTPS working

### Subdomains
- [ ] rafaelabs.xyz → Landing page
- [ ] dashboard.rafaelabs.xyz → Dashboard
- [ ] api.rafaelabs.xyz → API
- [ ] docs.rafaelabs.xyz → Docs
- [ ] beta.rafaelabs.xyz → Beta page
- [ ] demo.rafaelabs.xyz → Demo

### Email
- [ ] MX records configured
- [ ] SPF record added
- [ ] Email accounts created
- [ ] Test email sent/received
- [ ] Email signatures setup

### Security
- [ ] SSL/TLS enabled
- [ ] HTTPS redirect active
- [ ] Security headers configured
- [ ] DNSSEC enabled (optional)
- [ ] CAA records added (optional)

---

## 📊 Monitoring

### Uptime Monitoring
- **Service**: UptimeRobot (FREE)
- **Monitors**:
  - rafaelabs.xyz
  - dashboard.rafaelabs.xyz
  - api.rafaelabs.xyz
- **Alerts**: Email, Slack

### Analytics
- **Service**: Google Analytics (FREE)
- **Track**:
  - Page views
  - User behavior
  - Conversion rates
  - Traffic sources

### Performance
- **Service**: Cloudflare Analytics (FREE)
- **Metrics**:
  - Response time
  - Bandwidth usage
  - Cache hit rate
  - Threat detection

---

## 🔧 Maintenance

### Regular Tasks

#### Weekly
- [ ] Check uptime status
- [ ] Review analytics
- [ ] Monitor email deliverability

#### Monthly
- [ ] Review hosting costs
- [ ] Check SSL certificate expiry
- [ ] Update DNS records if needed
- [ ] Backup configurations

#### Annually
- [ ] Renew domain
- [ ] Review and optimize costs
- [ ] Update contact information
- [ ] Security audit

---

## 📞 Support Contacts

### Domain Support
- **Namecheap**: support.namecheap.com
- **Phone**: Available in dashboard
- **Chat**: 24/7 live chat

### Hosting Support
- **Railway**: railway.app/help
- **Vercel**: vercel.com/support
- **Cloudflare**: support.cloudflare.com

### Email Support
- **Zoho**: zoho.com/mail/help
- **Google Workspace**: support.google.com/a

---

## 🎉 Summary

### Current Status
✅ Domain registered: rafaelabs.xyz  
✅ Architecture designed  
✅ DNS plan ready  
✅ Email plan ready  
✅ Hosting plan ready  
✅ Cost calculated  

### Next Steps
1. Setup Cloudflare
2. Configure DNS records
3. Deploy dashboard to Railway
4. Deploy landing page to Vercel
5. Setup email accounts
6. Test all services
7. Enable monitoring

### Timeline
- **Day 1**: Cloudflare setup, DNS configuration
- **Day 2**: Deploy dashboard and landing page
- **Day 3**: Setup email, test everything
- **Day 4**: Enable monitoring, go live!

---

**🔱 RAFAEL Framework**  
*rafaelabs.xyz - Where systems evolve*

**Domain**: rafaelabs.xyz  
**Status**: REGISTERED ✅  
**Ready**: YES 🚀
