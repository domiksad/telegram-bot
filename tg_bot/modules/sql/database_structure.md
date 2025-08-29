### warnings
| chat_id | user_id | current_count |
| :---: | :---: | :---: |
| Int | Int | Int |

primary key (chat_id, user_id)

### channel_settings
| chat_id | language | max_warn_count | soft_warn |
| :---: | :---: | :---: | :---: |
| Int | Text | Int | Bool |
| NONE | DEFAULT_LANGUAGE | 3 | False |

if soft_warn is False than ban user after max_warn_count 
if soft_warn is True than kick user after max_warn_count