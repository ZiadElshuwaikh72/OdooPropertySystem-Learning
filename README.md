# OdooPropertySystem-Learning

App Name: app_one – Real Estate Module (Learning Project)  
Project Type: Educational / Learning Project

---

# Project Overview

This is a **Real Estate management module** built for Odoo 17.  
It is a personal learning project to practice Odoo module development, including models, views, security, reports, and OWL frontend components.  

The project is inspired by the Odoo 17 Development Course and applies concepts learned throughout the lessons.

---

# Features

- Manage Properties, Buildings, Owners , and Clients
- Track Property History and sales orders
- Custom Reports (PDF & XLSX)
- Frontend components using OWL for ListView and FormView
- Security rules for access control
- Wizards for changing states and managing workflows
- Multi-language support (`i18n`)

---

# Folder Structure
app_one/
├─ controllers/
│ ├─ init.py
│ ├─ property_api.py
│ └─ test_api.py
├─ models/
│ ├─ init.py
│ ├─ account_move.py
│ ├─ building.py
│ ├─ client.py
│ ├─ owner.py
│ ├─ property.py
│ ├─ property_history.py
│ ├─ res_partner.py
│ ├─ sale_order.py
│ └─ tag.py
├─ views/
│ ├─ account_move_view.xml
│ ├─ base_menu.xml
│ ├─ building_view.xml
│ ├─ owner_view.xml
│ ├─ property_history_view.xml
│ ├─ property_view.xml
│ ├─ res_partner_view.xml
│ ├─ sale_order_view.xml
│ └─ tag_view.xml
├─ reports/
│ ├─ init.py
│ ├─ property_report.xml
│ └─ xlsx_property_report.py
├─ wizard/
│ ├─ init.py
│ ├─ change_state_wizard.py
│ └─ change_state_wizard_view.xml
├─ security/
│ ├─ ir.model.access.csv
│ └─ security.xml
├─ static/
│ ├─ description/
│ │ └─ icon.png
│ └─ src/
│ ├─ components/
│ │ ├─ formView/
│ │ │ ├─ formView.css
│ │ │ ├─ formView.js
│ │ │ └─ formView.xml
│ │ └─ listView/
│ │ ├─ listView.css
│ │ ├─ listView.js
│ │ └─ listView.xml
│ └─ css/
│ ├─ font.css
│ └─ property.css
│ └─ fonts/
│ ├─ BitcountSingle_Roman-ExtraLight.ttf
│ └─ Tangerine-Regular.ttf
├─ data/
│ ├─ data.xml
│ └─ sequence.xml
├─ i18n/
│ ├─ app_one.pot
│ ├─ ar_001.mo
│ └─ ar_001.po
├─ init.py
├─ manifest.py
└─ .gitignore

