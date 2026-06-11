import sys, os
sys.path.insert(0, '.')
os.chdir('.')
from app.agents.copywriter import generate_post_node
result = generate_post_node({'topic': 'Messi', 'analysis_result': {'key_insights': ['14 goals']}, 'style_context': 'Bengali sports', 'raw_data': {}})
err = result.get('error')
posts = result.get('bangla_posts', [])
print(f'posts={len(posts)}, error={err}')
if posts:
    print('Preview:', posts[0].content[:80])
