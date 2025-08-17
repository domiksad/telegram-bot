### warnings
| chat_id | user_id | current_count |
| :---: | :---: | :---: |
| Int | Int | Int |

primary key (chat_id, user_id)

### messages
| chat_id | message_id | user_id | sent_at |
| :---: | :---: | :---: | :---: |
| Int | Int | Int | Timestamp |

primary key (chat_id, message_id)

### rules
| chat_id | rule_text |
| :---: | :---: |
| int | str

primary key (chat_id)