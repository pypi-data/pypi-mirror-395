# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated data pipeline processing.

## Available Workflows

### 1. Data Pipeline Processing (`data-pipeline.yml`)

**Manual workflow** for running data pipelines on-demand with full control over parameters.

**Trigger**: Manual via GitHub Actions UI (workflow_dispatch)

**Features**:
- ✅ Run compliance pipeline, knowledge pipeline, or both
- ✅ Select specific compliance standard or process all
- ✅ Choose pipeline mode (streaming or checkpointing)
- ✅ Skip collection stage (use existing raw data)
- ✅ Limit URLs for knowledge pipeline (for testing)
- ✅ Upload logs and checkpoint files as artifacts

**How to Use**:
1. Go to **Actions** tab in GitHub
2. Select **Data Pipeline Processing** workflow
3. Click **Run workflow**
4. Configure parameters:
   - **Pipeline type**: compliance, knowledge, or both
   - **Standard**: Leave empty for all, or specify (e.g., PCI-DSS)
   - **Domain**: For knowledge pipeline (e.g., compliance)
   - **Mode**: streaming (production) or checkpointing (debug)
   - **Skip collection**: Check to skip collection stage
   - **Limit URLs**: For knowledge pipeline testing (0 = no limit)
5. Click **Run workflow**

**Example Configurations**:

**Process single compliance standard**:
- Pipeline type: `compliance`
- Standard: `PCI-DSS`
- Mode: `streaming`

**Process all compliance standards**:
- Pipeline type: `compliance`
- Standard: (leave empty)
- Mode: `streaming`

**Process knowledge base**:
- Pipeline type: `knowledge`
- Domain: `compliance`
- Mode: `streaming`

**Process all knowledge domains**:
- Pipeline type: `knowledge`
- Domain: `all`
- Mode: `streaming`

**Test with limited URLs**:
- Pipeline type: `knowledge`
- Domain: `compliance`
- Limit URLs: `10`
- Mode: `streaming`

---

### 2. Scheduled Data Pipeline (`scheduled-pipeline.yml`)

**Automated workflow** that runs daily to update data pipelines.

**Trigger**: 
- Automatic: Daily at 2 AM UTC (via cron schedule)
- Manual: Can also be triggered manually via workflow_dispatch

**Features**:
- ✅ Runs compliance pipeline for all standards
- ✅ Runs knowledge pipeline for compliance domain
- ✅ Uses streaming mode (production)
- ✅ Uploads logs as artifacts

**Schedule**: Daily at 2 AM UTC (`0 2 * * *`)

**To modify schedule**: Edit the cron expression in `scheduled-pipeline.yml`:
```yaml
schedule:
  - cron: '0 2 * * *'  # Change this to your preferred time
```

**Cron format**: `minute hour day month weekday`
- `0 2 * * *` = Daily at 2 AM UTC
- `0 */6 * * *` = Every 6 hours
- `0 0 * * 0` = Weekly on Sunday at midnight

---

## Required Secrets

Both workflows require the following GitHub Secrets to be configured:

### Required Secrets

1. **`OPENAI_API_KEY`** (Required)
   - OpenAI API key for generating embeddings
   - Get from: https://platform.openai.com/api-keys

2. **`MONGODB_URL`** (Required)
   - MongoDB connection string (from your `.env` file)
   - Example: `mongodb://username:password@host:port/database`
   - Or: `mongodb+srv://username:password@cluster.mongodb.net/database`

3. **`MONGODB_DATABASE`** (Optional, defaults to `wistx-production`)
   - MongoDB database name
   - Default: `wistx-production`

4. **`PINECONE_API_KEY`** (Required)
   - Pinecone API key for vector storage
   - Get from: https://app.pinecone.io/

5. **`PINECONE_INDEX_NAME`** (Optional, defaults to `wistx-index`)
   - Name of Pinecone index to use
   - Default: `wistx-index`

### Optional Secrets

6. **`TAVILY_API_KEY`** (Optional)
   - Tavily API key for web search integration
   - Get from: https://tavily.com/

### How to Add Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its name and value
5. Click **Add secret**

---

## Workflow Artifacts

Both workflows upload artifacts that you can download:

### Logs
- **Name**: `pipeline-logs` or `scheduled-pipeline-logs`
- **Contents**: All log files from pipeline execution
- **Retention**: 7 days

### Checkpoint Files (checkpointing mode only)
- **Name**: `checkpoint-files`
- **Contents**: Raw data, processed data, embeddings
- **Retention**: 7 days

**To download artifacts**:
1. Go to **Actions** tab
2. Click on the workflow run
3. Scroll to **Artifacts** section
4. Click artifact name to download

---

## MongoDB Configuration

Both workflows use your existing MongoDB instance configured via secrets:

- **Connection**: Uses `MONGODB_URL` secret from your `.env` file
- **Database**: Uses `MONGODB_DATABASE` secret (defaults to `wistx-production`)
- **Setup**: Runs `setup_mongodb.py` to initialize collections and indexes

**Important**: Make sure your MongoDB instance is accessible from GitHub Actions runners (public IP or VPN).

---

## Timeout Settings

- **Manual Pipeline**: 120 minutes timeout
- **Scheduled Pipeline**: 180 minutes timeout

If your pipeline takes longer, you can increase the timeout in the workflow file:
```yaml
timeout-minutes: 180  # Increase as needed
```

---

## Troubleshooting

### Workflow Fails with "MongoDB connection error"

- Verify `MONGODB_URL` secret is set correctly (copy from your `.env` file)
- Check MongoDB instance is accessible from GitHub Actions runners (public IP or VPN)
- Verify MongoDB credentials are correct
- Check workflow logs for detailed error messages
- Ensure MongoDB firewall allows connections from GitHub Actions IP ranges

### Workflow Fails with "OpenAI API error"

- Verify `OPENAI_API_KEY` secret is set correctly
- Check OpenAI API quota/limits
- Review API error messages in workflow logs

### Workflow Fails with "Pinecone error"

- Verify `PINECONE_API_KEY` secret is set correctly
- Check `PINECONE_INDEX_NAME` matches your Pinecone index
- Verify Pinecone index exists and is accessible

### Workflow Takes Too Long

- Use `--no-collection` flag to skip collection stage
- Process single standard instead of all
- Use `limit_urls` parameter for knowledge pipeline
- Increase timeout in workflow file

---

## Best Practices

1. **Test First**: Use manual workflow with single standard before running all
2. **Monitor Logs**: Check workflow logs for errors and warnings
3. **Use Checkpointing**: Enable checkpointing mode for debugging
4. **Limit URLs**: Use `limit_urls` parameter for testing knowledge pipeline
5. **Review Artifacts**: Download and review logs/checkpoint files

---

## Workflow Status

You can check workflow status:
- **Green checkmark**: Success
- **Red X**: Failure (check logs)
- **Yellow circle**: In progress
- **Gray circle**: Cancelled

---

## Customization

To customize workflows:

1. **Change schedule**: Edit cron expression in `scheduled-pipeline.yml`
2. **Add more domains**: Add to domain choices in `data-pipeline.yml`
3. **Modify timeout**: Change `timeout-minutes` value
4. **Add notifications**: Add Slack/Discord/Email notifications on failure

---

**Need Help?** Check the main documentation:
- `PIPELINE_QUICK_START.md` - Local pipeline execution guide
- `README.md` - General project documentation

