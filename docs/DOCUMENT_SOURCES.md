# Document Sources for UK Name Change After Marriage

## Recommended Official Documents

### 1. **GOV.UK - Official Government Guidance**
- **URL**: https://www.gov.uk/change-name-deed-poll
- **URL**: https://www.gov.uk/change-name-marriage-divorce
- **Why**: Primary source for official name change procedures
- **Format**: HTML web pages (can be scraped or saved as PDF)

### 2. **DVLA (Driver and Vehicle Licensing Agency)**
- **URL**: https://www.gov.uk/change-address-driving-licence
- **URL**: https://www.gov.uk/exchange-driving-licence
- **Why**: Essential for updating driving licence after name change
- **Format**: Web pages, downloadable PDF forms

### 3. **HM Passport Office**
- **URL**: https://www.gov.uk/apply-renew-passport
- **URL**: https://www.gov.uk/changing-passport-information
- **Why**: Required for passport updates after marriage
- **Format**: Web pages, application forms

### 4. **Marriage Certificate Information**
- **URL**: https://www.gov.uk/marriage-certificates
- **Why**: Marriage certificate is the key document needed for name changes
- **Format**: Web pages

### 5. **Electoral Roll Updates**
- **URL**: https://www.gov.uk/register-to-vote
- **Why**: Important for maintaining voting registration
- **Format**: Web pages

### 6. **HM Revenue and Customs (HMRC)**
- **URL**: https://www.gov.uk/tell-hmrc-change-of-details
- **Why**: Tax records need updating
- **Format**: Web pages

### 7. **Banks and Financial Services**
- **URL**: Various (not government, but important)
- **Why**: Banks require name updates
- **Format**: General guidance pages

## Document Acquisition Strategy

### Option 1: Manual Download (Recommended for MVP)
1. Visit each URL
2. Save pages as PDF or HTML
3. Store in `data/raw/` directory
4. Process and index

### Option 2: Web Scraping (For Automation)
- Use tools like `beautifulsoup4` or `scrapy`
- Respect robots.txt and rate limits
- Save structured content

### Option 3: Official API (If Available)
- Check GOV.UK API: https://www.gov.uk/api
- May have structured data endpoints

## Document Organization

```
data/
├── raw/                    # Original downloaded documents
│   ├── govuk/
│   ├── dvla/
│   ├── passport/
│   └── marriage/
├── processed/              # Cleaned and processed text
└── indexed/                # Ready for indexing (optional)
```

## Priority Order

1. **High Priority** (Essential):
   - GOV.UK name change overview
   - Marriage certificate requirements
   - DVLA driving licence update
   - Passport Office update

2. **Medium Priority** (Important):
   - Electoral roll
   - HMRC updates
   - Bank updates (general guidance)

3. **Low Priority** (Nice to have):
   - Utility companies
   - Insurance providers
   - Employer records
