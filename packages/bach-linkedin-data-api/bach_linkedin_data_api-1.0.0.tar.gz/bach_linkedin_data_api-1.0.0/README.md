# Linkedin Data Api MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Linkedin Data Api API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-linkedin_data_api`）
5. 🎉 点击 **"安装 MCP"** 按钮
6. ✅ 完成！即可在您的应用中使用

### EMCP 平台优势：

- ✨ **零配置**：无需手动编辑配置文件
- 🎨 **可视化管理**：图形界面轻松管理所有 MCP 服务器
- 🔐 **安全可靠**：统一管理 API 密钥和认证信息
- 🚀 **一键安装**：MCP 广场提供丰富的服务器选择
- 📊 **使用统计**：实时查看服务调用情况

立即访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)** 开始您的 MCP 之旅！


---

## 简介

这是一个 MCP 服务器，用于访问 Linkedin Data Api API。

- **PyPI 包名**: `bach-linkedin_data_api`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-linkedin_data_api
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-linkedin_data_api bach_linkedin_data_api

# 或指定版本
uvx --from bach-linkedin_data_api@latest bach_linkedin_data_api
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-linkedin_data_api

# 运行（命令名使用下划线）
bach_linkedin_data_api
```

## 配置

### API 认证

此 API 需要认证。请设置环境变量:

```bash
export API_KEY="your_api_key_here"
```

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `API_KEY` | API 密钥 | 是 |
| `PORT` | 不适用 | 否 |
| `HOST` | 不适用 | 否 |



### 在 Cursor 中使用

编辑 Cursor MCP 配置文件 `~/.cursor/mcp.json`:


```json
{
  "mcpServers": {
    "bach-linkedin_data_api": {
      "command": "uvx",
      "args": ["--from", "bach-linkedin_data_api", "bach_linkedin_data_api"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 在 Claude Desktop 中使用

编辑 Claude Desktop 配置文件 `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bach-linkedin_data_api": {
      "command": "uvx",
      "args": ["--from", "bach-linkedin_data_api", "bach_linkedin_data_api"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `get_company_by_domain`

Enrich the company data by domain. **1 credit per successful request.**

**端点**: `GET /get-company-by-domain`


**参数**:

- `domain` (string) *必需*: Example value: apple.com



---


### `get_company_details_by_id`

The endpoint enrich full details of the company

**端点**: `GET /get-company-details-by-id`


**参数**:

- `id` (string) *必需*: Example value: 1441



---


### `get_company_details`

The endpoint enrich full details of the company

**端点**: `GET /get-company-details`


**参数**:

- `username` (string) *必需*: Example value: google



---


### `get_profile_school_interests`

Get the profile's school interests up to 50 results per page

**端点**: `POST /profiles/interests/schools`



---


### `get_profile_newsletter_interests`

Get the profile's newsletter interests up to 50 results per page

**端点**: `POST /profiles/interests/newsletters`



---


### `get_similar_profiles`

Returns profiles that are similar to the provided profile

**端点**: `GET /similar-profiles`


**参数**:

- `url` (string) *必需*: Example value: https://www.linkedin.com/in/williamhgates/



---


### `get_profile_positions_with_skills`

Get Profile Positions With Skills

**端点**: `GET /profiles/position-skills`


**参数**:

- `username` (string) *必需*: Example value: tedgaubert



---


### `get_profile_company_interest`

Get the profile's company interests up to 50 results per page.

**端点**: `POST /profiles/interests/companies`



---


### `profile_data_u0026_recommendations`

Get Profile Data, Given and Received Recommendations. **2 credits per call**

**端点**: `GET /all-profile-data`


**参数**:

- `username` (string) *必需*: Example value: ryanroslansky



---


### `get_given_recommendations`

To scrape all recommendations from a profile, increase the start value to +100 for each request until you reach the total recommendations count. You can find the total recommendations count in the response

**端点**: `GET /get-given-recommendations`


**参数**:

- `username` (string) *必需*: Example value: ryanroslansky

- `start` (string): Example value: 0



---


### `get_profile_data_connection_u0026_follower_count_and_posts`

Get Profile Data, Connection \u0026 Follower Count and Posts. 2 credits per call

**端点**: `GET /profile-data-connection-count-posts`


**参数**:

- `username` (string) *必需*: Example value: adamselipsky



---


### `about_the_profile`

Get profile verification details, profile’s joined, contact information updated, and profile photo updated date

**端点**: `GET /about-this-profile`


**参数**:

- `username` (string) *必需*: Example value: williamhgates



---


### `get_profile_data_and_connection_u0026_follower_count`

Get Profile Data and Connection \u0026 Follower Count

**端点**: `GET /data-connection-count`


**参数**:

- `username` (string) *必需*: Example value: adamselipsky



---


### `get_received_recommendations`

To scrape all recommendations from a profile, increase the start value to +100 for each request until you reach the total recommendations count. You can find the total recommendations count in the response

**端点**: `GET /get-received-recommendations`


**参数**:

- `username` (string) *必需*: Example value: ryanroslansky

- `start` (string): Example value: 0



---


### `get_profiles_comments`

Get last 50 comments of a profile. 1 credit per call

**端点**: `GET /get-profile-comments`


**参数**:

- `username` (string) *必需*: Example value: williamhgates



---


### `get_profile_reactions`

Find out what posts a profile reacted to

**端点**: `GET /get-profile-likes`


**参数**:

- `username` (string) *必需*: Example value: adamselipsky

- `start` (string): for pagination, increase +100 to parse next result until you see less than 100 results. it could be one of these; 0, 100, 200, 300, 400, etc.

- `paginationToken` (string): It is required when fetching the next results page. The token from the previous call must be used.



---


### `get_profile_post_and_comments`

Get profile post and comments of the post

**端点**: `GET /get-profile-post-and-comments`


**参数**:

- `urn` (string) *必需*: URN value of the post. Example URL: https://www.linkedin.com/posts/andy-jassy-8b1615_amazon-bedrock-customers-have-more-choice-activity-7181285160586211328-Idxl/?utm_source=share&utm_medium=member_desktop Example URN: 7181285160586211328



---


### `get_profile_connection_u0026_follower_count`

Get Profile Connection \u0026 Follower Count

**端点**: `GET /connection-count`


**参数**:

- `username` (string) *必需*: Example value: adamselipsky



---


### `get_profile_post_comment`

Get 50 comments of a profile post  (activity)

**端点**: `GET /get-profile-posts-comments`


**参数**:

- `urn` (string) *必需*: Post urn value

- `sort` (string) *必需*: it could be one of these; mostRelevant, mostRecent

- `page` (string): Example value: 1

- `paginationToken` (string): It is required when fetching the next results page. The token from the previous call must be used.



---


### `search_people_by_url`

Search profiles by a keyword. You may see less than 10 results per page. This is because not return all profiles as public, sometimes hiding profiles and these profiles appear in the result. The endpoint automatically filters these profiles from the result

**端点**: `POST /search-people-by-url`



---


### `get_profile_data`

Enrich profile data, including experience,  skills, language and companies.

**端点**: `GET /`


**参数**:

- `username` (string) *必需*: Example value: adamselipsky



---


### `search_people`

Search profiles by a keyword. You may see less than 10 results per page. This is because not return all profiles as public, sometimes hiding profiles and these profiles appear in the result. The endpoint automatically filters these profiles from the result

**端点**: `GET /search-people`


**参数**:

- `keywords` (string): Example value: max

- `start` (string): it could be one of these; 0, 10, 20, 30, etc.

- `geo` (string): please follow this link to find location id

- `schoolId` (string): Example value: 

- `firstName` (string): Example value: 

- `lastName` (string): Example value: 

- `keywordSchool` (string): Example value: 

- `keywordTitle` (string): Example value: 

- `company` (string): Company name



---


### `get_profile_data_by_url`

Get all profile data, including experience,  skills, language, education, course, and companies, **open to work** status, hiring status, location. Check **Example Responses** for more details

**端点**: `GET /get-profile-data-by-url`


**参数**:

- `url` (string) *必需*: Example value: https://www.linkedin.com/in/adamselipsky/



---


### `get_profile_group_interests`

Get the profile's group interests up to 50 results per page

**端点**: `POST /profiles/interests/groups`



---


### `get_profile_top_voice_interests`

Get the profile's top voices interests

**端点**: `POST /profiles/interests/top-voices`



---


### `get_profiles_posts`

Get last 50 posts of a profile. 1 credit per call

**端点**: `GET /get-profile-posts`


**参数**:

- `username` (string) *必需*: Example value: adamselipsky

- `start` (string): use this param to get posts in next results page: 0 for page 1, 50 for page 2 100 for page 3, etc.

- `paginationToken` (string): It is required when fetching the next results page. The token from the previous call must be used.

- `postedAt` (string): It is not an official filter. It filters posts after fetching them from LinkedIn and returns posts that are newer than the given date. Example value: 2024-01-01 00:00



---


### `get_post_reactions`

Get profiles that reacted to the post

**端点**: `POST /get-post-reactions`



---


### `get_profile_top_position`

Get profile top position

**端点**: `GET /profiles/positions/top`


**参数**:

- `username` (string) *必需*: Example value: adamselipsky



---


### `get_companys_post`

Get last 50 posts of a company. 1 credit per call

**端点**: `GET /get-company-posts`


**参数**:

- `username` (string) *必需*: Example value: microsoft

- `start` (string): use this param to get posts in next results page: 0 for page 1, 50 for page 2, 100 for page 3, etc.

- `paginationToken` (string): It is required when fetching the next results page. The token from the previous call must be used.



---


### `get_company_pages_people_also_viewed`

Get Company Pages People Also Viewed

**端点**: `GET /get-company-pages-people-also-viewed`


**参数**:

- `username` (string): Example value: google



---


### `get_company_insights_premium`

Get Company Insight Details \u0026 Company Details in a single request. **5 credit per call.** If the request fails, you don't pay.

**端点**: `GET /get-company-insights`


**参数**:

- `username` (string) *必需*: Example value: amazon



---


### `search_posts`

Search Posts

**端点**: `POST /search-posts`



---


### `search_jobs_v2`

Search Jobs

**端点**: `GET /search-jobs-v2`


**参数**:

- `keywords` (string) *必需*: Example value: golang

- `locationId` (number): please follow this link to find location id

- `companyIds` (string): please follow this link to find company id

- `datePosted` (string): it could be one of these; anyTime, pastMonth, pastWeek, past24Hours

- `salary` (string): it could be one of these; 40k+, 60k+, 80k+, 100k+, 120k+, 140k+, 160k+, 180k+, 200k+ Example: 80k+

- `jobType` (string): it could be one of these; fullTime, partTime, contract, internship Example: contract

- `experienceLevel` (string): it could be one of these; internship, associate, director, entryLevel, midSeniorLevel. executive example: executive

- `titleIds` (string): please follow this link to find title id by title

- `functionIds` (string): please follow this link to find function id

- `start` (string): it could be one of these; 0, 50, 100, 150, 200, etc. The maximum number of start is 975

- `industryIds` (string): please follow this link to find industry id

- `onsiteRemote` (string): it could be one of these; onSite remote hybrid example: remote

- `sort` (string): it could be one of these; mostRelevant, mostRecent

- `distance` (string): 0 = 0km 5 = 8km 10 = 16km 25 = 40km 50 = 80km 100 = 160km



---


### `get_profiles_posted_jobs`

Get profile's posted jobs.

**端点**: `GET /profiles/posted-jobs`


**参数**:

- `username` (string) *必需*: LinkedIn job id



---


### `get_company_post_comments`

Get comments of a company post

**端点**: `GET /get-company-post-comments`


**参数**:

- `urn` (string) *必需*: Example value: 7179144327430844416

- `sort` (string) *必需*: Example value: mostRelevant

- `page` (string): Example value: 1



---


### `get_company_employees_count`

Get company employees count (location filter possible)

**端点**: `POST /get-company-employees-count`



---


### `search_companies`

Search companies

**端点**: `POST /companies/search`



---


### `get_job_details`

Get the full job details, including the job skills and the company information

**端点**: `GET /get-job-details`


**参数**:

- `id` (number) *必需*: Example value: 4090994054



---


### `get_article_comments`

Get article comments with url

**端点**: `GET /get-article-comments`


**参数**:

- `url` (string) *必需*: Example value: https://www.linkedin.com/pulse/2024-corporate-climate-pivot-bill-gates-u89mc/?trackingId=V85mkekwT9KruOXln2gzIg%3D%3D

- `page` (string): Example value: 1

- `sort` (string): Example value: REVERSE_CHRONOLOGICAL



---


### `get_article_reactions`

Get article reactions with url

**端点**: `GET /get-article-reactions`


**参数**:

- `url` (string) *必需*: Example value: https://www.linkedin.com/pulse/2024-corporate-climate-pivot-bill-gates-u89mc/?trackingId=V85mkekwT9KruOXln2gzIg%3D%3D

- `page` (string): Example value: 1



---


### `get_article`

Get article with url

**端点**: `GET /get-article`


**参数**:

- `url` (string) *必需*: Example value: https://www.linkedin.com/pulse/hidden-costs-unreliable-electricity-bill-gates/



---


### `get_user_articles`

Get user articles by profile with url or username

**端点**: `GET /get-user-articles`


**参数**:

- `url` (string): Example value: https://www.linkedin.com/in/williamhgates/

- `username` (string): Example value: williamhgates



---


### `get_post_reposts`

Get post reposts by post url

**端点**: `POST /posts/reposts`



---


### `get_post`

Get post details

**端点**: `GET /get-post`


**参数**:

- `url` (string) *必需*: Example value: https://www.linkedin.com/feed/update/urn:li:activity:7219434359085252608/



---


### `get_company_jobs`

Get company jobs

**端点**: `POST /company-jobs`



---


### `search_jobs`

Search Jobs

**端点**: `GET /search-jobs`


**参数**:

- `keywords` (string) *必需*: Example value: golang

- `locationId` (number): please follow this link to find location id

- `companyIds` (string): please follow this link to find company id

- `datePosted` (string): it could be one of these; anyTime, pastMonth, pastWeek, past24Hours

- `salary` (string): it could be one of these; 40k+, 60k+, 80k+, 100k+, 120k+, 140k+, 160k+, 180k+, 200k+ Example: 80k+

- `jobType` (string): it could be one of these; fullTime, partTime, contract, internship Example: contract

- `experienceLevel` (string): it could be one of these; internship, associate, director, entryLevel, midSeniorLevel. executive example: executive

- `titleIds` (string): please follow this link to find title id by title

- `functionIds` (string): please follow this link to find function id

- `start` (string): it could be one of these; 0, 25, 50, 75, 100, etc. The maximum number of start is 975

- `industryIds` (string): please follow this link to find industry id

- `onsiteRemote` (string): it could be one of these; onSite remote hybrid example: remote

- `sort` (string): it could be one of these; mostRelevant, mostRecent



---


### `health_check`

Health Check

**端点**: `GET /health`



---


### `get_hiring_team`

Get hiring team/job poster profile details. You can use either a job id or a job URL. One of these is required.

**端点**: `GET /get-hiring-team`


**参数**:

- `id` (string): LinkedIn job id

- `url` (string): LinkedIn job url



---


### `search_locations`

Search locations by keyword

**端点**: `GET /search-locations`


**参数**:

- `keyword` (string) *必需*: Example value: berlin



---


### `search_post_by_hashtag`

Search Post by Hashtag

**端点**: `POST /search-posts-by-hashtag`



---


### `get_company_jobs_count`

Get total number of opening jobs the company

**端点**: `GET /get-company-jobs-count`


**参数**:

- `companyId` (string) *必需*: Example value: 1441



---


### `get_profile_recent_activity_time`

Get the time of the profile's last activity

**端点**: `GET /get-profile-recent-activity-time`


**参数**:

- `username` (string) *必需*: Example value: adamselipsky



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
