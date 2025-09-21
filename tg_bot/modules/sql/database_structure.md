### warnings
| chat_id | user_id | current_count |
| :---: | :---: | :---: |
| Int | Int | Int |

primary key (chat_id, user_id)

### channel_settings
| chat_id | language | max_warn_count | soft_warn | change_settings_creator_only | welcome_message_json |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Int | Text | Int | Bool | Bool | Text |
| NONE | DEFAULT_LANGUAGE | 3 | False | True | "" |

if soft_warn is False than ban user after max_warn_count 
if soft_warn is True than kick user after max_warn_count
welcome_message format: {"type": "", "content": ""}

### groups
| chat_id |
| :---: |
| Int |