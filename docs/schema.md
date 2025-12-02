# Database Schema

Database entities and their relationships.

## 1. Organizations

Describes organizations where users belong.

### Columns

| Column | Type | Constraints |
|--------|------|-------------|
| id | bigint | Primary key |
| name | string | Required, Optional index |
| created_at | timestamp | Default: now |
| updated_at | timestamp | Auto-updated on change |
| deleted_at | timestamp | Soft delete |

## 2. Users

Describes lender side users.

### Columns

| Column | Type | Constraints |
|--------|------|-------------|
| id | bigint | Primary key |
| organization_id | bigint | Foreign key → organizations.id |
| email | string | Required, Unique |
| hashed_password | string | Required |
| first_name | string | |
| last_name | string | |
| role | string or enum | |
| is_active | boolean | Default: true |
| created_at | timestamp | |
| updated_at | timestamp | |
| deleted_at | timestamp | Nullable |

## 3. Borrowers

Describes borrowers whose 1003 applications are being managed.

### Columns

| Column | Type | Constraints |
|--------|------|-------------|
| id | bigint | Primary key |
| organization_id | bigint | Foreign key → organizations.id |
| email | string | Nullable |
| phone | string | Nullable |
| first_name | string | |
| last_name | string | |
| ssn_last_4 | string | |
| created_at | timestamp | |
| linked_user | bigint | Foreign key → users.id, Nullable |
| updated_at | timestamp | |
| deleted_at | timestamp | Nullable |

## 4. Applications

Describes 1003 applications.

### Columns

| Column | Type | Constraints |
|--------|------|-------------|
| id | bigint | Primary key |
| organization_id | bigint | Foreign key → organizations.id, Indexed |
| borrower_id | bigint | Foreign key → borrowers.id, Indexed |
| loan_number | string | Nullable |
| loan_amount | numeric | |
| status | string or enum | Indexed |
| raw_1003 | json or jsonb | |
| created_at | timestamp | |
| updated_at | timestamp | |
| deleted_at | timestamp | Nullable |

## 5. Documents

Uploaded documents tied to an application.

### Columns

| Column | Type | Constraints |
|--------|------|-------------|
| id | bigint | Primary key |
| organization_id | bigint | Foreign key → organizations.id, Indexed |
| application_id | bigint | Foreign key → applications.id, Indexed |
| uploaded_by_user_id | bigint | Foreign key → users.id |
| file_name | string | |
| storage_path | string | |
| document_type | string or enum | |
| mime_type | string | |
| uploaded_at | timestamp | |
| deleted_at | timestamp | Nullable |

## Relationships

- **Organization**
  - has many Users
  - has many Borrowers
  - has many Applications
  - has many Documents

- **User**
  - belongs to Organization
  - uploads many Documents

- **Borrower**
  - belongs to Organization
  - has many Applications

- **Application**
  - belongs to Organization
  - belongs to Borrower
  - has many Documents

- **Document**
  - belongs to Organization
  - belongs to Application
  - belongs to User (uploader)