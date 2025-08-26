### warnings
| chat_id | user_id | current_count |
| :---: | :---: | :---: |
| Int | Int | Int |

primary key (chat_id, user_id)

### channel_settings
| chat_id | language |
| :---: | :---: |
| Int | Text |
| NONE | DEFAULT_LANGUAGE |