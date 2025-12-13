# Clients API Droit

## Install 

Install from local cloned repo using `pip install -e path/to/py-clients-api-droit`.


## Usage

### Légifrance

```python
from clients_api_droit.legifrance import (
    LegifranceClient, LegifranceSettings, authenticate, iter_articles, get_article, get_code_summary
)

client = LegifranceClient(
    settings=LegifranceSettings(
        client_id='LEGIFRANCE_CLIENT_ID',
        client_secret='LEGIFRANCE_CLIENT_SECRET',
    )
)

# Authenticate to légifrance API
client = authenticate(client)

# Get the summary of the code de l'environnement
code_environnement = get_code_summary(client, "LEGITEXT000006074220")

# Iterate over the first 10 articles in the code
for i, (parent_sections, article) in enumerate(iter_articles([code_environnement])):
    if i == 10:
        break

    # Get the full article data
    article_full = get_article(client, article['id'])

    # Print its title number and text
    print('\n\nCode de l\'environnement - ' + article_full['article']['num'])
    print(article_full['article']['texte'])
```

### EURLex

```python
from clients_api_droit.eurlex import (
    EurlexClient, EurlexSettings, search_act
)

client = EurlexClient(
    settings=EurlexSettings(
        web_service_username=os.environ['EURLEX_WEB_SERVICE_USERNAME'],
        web_service_password=os.environ['EURLEX_WEB_SERVICE_PASSWORD'],
    )
)

print('regulation 1996/2', list(search_act(client, 'regulation', 1996, 2)))
print('directive 2010/75', list(search_act(client, 'directive', 2010, 75)))
print('decision 2023/10', list(search_act(client, 'decision', 2023, 10)))
print('regulation 2003/87', list(search_act(client, 'regulation', 2003, 87)))
```
