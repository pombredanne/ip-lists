# IP Lists

Common IP lists in a format friendly to importing into Deep Security.

## Usage

```bash
./get_latest_ips_from_aws.py
```

This will generate a set of XML IP lists for import into Deep Security. You can import each individually or the entire set via "YYY-mmm-ddd-all-aws-public-ips.xml".

## Importing

Within the Deep Security admin interface:

1. Click on the "Policies" button
1. Expand the "Common Objects" entry on the left hand side
1. Expand the "Lists" entry on the left hand side
1. Select "IP Lists" from the left hand side<sup>1</sup>
1. Click the "New" button and select "Import From File..."
1. Follow the steps presented by the import wizard

![Deep Security importing an IP list](/docs/deep-security-ip-list-import.png)
<sup>1</sup>
