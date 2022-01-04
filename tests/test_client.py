import re
import pytest
from ewhs.exceptions import AuthenticationError

# TODO: Increase amount of tests

def test_client_default_user_agent(client, response):
    """Default user-agent should contain some known values."""
    regex = re.compile(r"^Ewarehousing/[\d\.]+ Python/[\w\.\+]+$")
    assert re.match(regex, client.user_agent)

    # perform a request and inspect the actual used headers
    response.get("https://api.ewarehousing.com/api/orders", "order_list")
    response.post("https://api.ewarehousing.com/api/wms/auth/login", "auth_login")
    client.order.list()
    request = response.calls[0].request
    assert re.match(regex, request.headers["User-Agent"])


def test_client_auth(client, response):
    assert client.access_token is None
    assert client.refresh_token is None
    assert client.expires_at is 0

    response.post("https://api.ewarehousing.com/api/wms/auth/login", "auth_login")
    response.post("https://api.ewarehousing.com/api/wms/auth/refresh", "auth_login_refresh")
    response.get("https://api.ewarehousing.com/api/orders", "order_list")

    client.order.list()

    # Auth after login
    assert client.access_token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2Mzg1NDM1NzUsImV4cCI6MTYzODU0NzE3NSwicm9sZXMiOlsiUk9MRV9TQ0FOTkVSIiwiUk9MRV9EQVNIQk9BUkRfUkVBRCIsIlJPTEVfREFTSEJPQVJEX1NUQVRVUyIsIlJPTEVfU1RPQ0tfUkVBRCIsIlJPTEVfU1RPQ0tfSU1QT1JUIiwiUk9MRV9TVE9DS19FWFBPUlQiLCJST0xFX1NUT0NLSElTVE9SWV9SRUFEIiwiUk9MRV9TVE9DS0hJU1RPUllfRVhQT1JUIiwiUk9MRV9NT0RJRklDQVRJT05fUkVBRCIsIlJPTEVfTU9ESUZJQ0FUSU9OX0NSRUFURSIsIlJPTEVfTU9ESUZJQ0FUSU9OX1VQREFURSIsIlJPTEVfTU9ESUZJQ0FUSU9OX0FQUFJPVkUiLCJST0xFX01PRElGSUNBVElPTl9FWFBPUlQiLCJST0xFX1RSQU5TRkVSX1JFQUQiLCJST0xFX1RSQU5TRkVSX0NSRUFURSIsIlJPTEVfVFJBTlNGRVJfVVBEQVRFIiwiUk9MRV9UUkFOU0ZFUl9ERUxFVEUiLCJST0xFX1RSQU5TRkVSX0NBTkNFTCIsIlJPTEVfVFJBTlNGRVJfVU5IT0xEIiwiUk9MRV9UUkFOU0ZFUl9VTkFTU0lHTiIsIlJPTEVfVFJBTlNGRVJfUkVWSUVXIiwiUk9MRV9UUkFOU0ZFUl9FWFBPUlQiLCJST0xFX0FSVElDTEVfUkVBRCIsIlJPTEVfQVJUSUNMRV9DUkVBVEUiLCJST0xFX0FSVElDTEVfVVBEQVRFX0JBUkNPREVTIiwiUk9MRV9BUlRJQ0xFX1VQREFURSIsIlJPTEVfQVJUSUNMRV9ERUxFVEUiLCJST0xFX0FSVElDTEVfSU1QT1JUIiwiUk9MRV9BUlRJQ0xFX1VQREFURV9ET0NVTUVOVFMiLCJST0xFX0FSVElDTEVfRVhQT1JUIiwiUk9MRV9WQVJJQU5UX1FVQVJBTlRJTkUiLCJST0xFX1NVUFBMSUVSX1JFQUQiLCJST0xFX1NVUFBMSUVSX0NSRUFURSIsIlJPTEVfU1VQUExJRVJfVVBEQVRFIiwiUk9MRV9TVVBQTElFUl9ERUxFVEUiLCJST0xFX0lOQk9VTkRfUkVBRCIsIlJPTEVfSU5CT1VORF9DUkVBVEUiLCJST0xFX0lOQk9VTkRfVVBEQVRFIiwiUk9MRV9JTkJPVU5EX0NBTkNFTCIsIlJPTEVfSU5CT1VORF9QUk9DRVNTIiwiUk9MRV9JTkJPVU5EX0NPTVBMRVRFIiwiUk9MRV9JTkJPVU5EX0VYUE9SVCIsIlJPTEVfT1JERVJfUkVBRCIsIlJPTEVfT1JERVJfQ1JFQVRFIiwiUk9MRV9PUkRFUl9VUERBVEUiLCJST0xFX09SREVSX1VQREFURV9QUk9DRVNTSU5HIiwiUk9MRV9PUkRFUl9VUERBVEVfUEFBWkwiLCJST0xFX09SREVSX1BBUlRJQUwiLCJST0xFX09SREVSX1VOSE9MRCIsIlJPTEVfT1JERVJfQ0FOQ0VMIiwiUk9MRV9PUkRFUl9DQU5DRUxfUFJPQ0VTU0lORyIsIlJPTEVfT1JERVJfUFJPQkxFTSIsIlJPTEVfT1JERVJfRVhQT1JUIiwiUk9MRV9PUkRFUl9QUklPUklUSVpFIiwiUk9MRV9PUkRFUl9JTVBPUlQiLCJST0xFX1BJQ0tMSVNUX1JFQUQiLCJST0xFX1BJQ0tMSVNUX0VYUE9SVCIsIlJPTEVfUElDS0xJU1RfVU5BU1NJR04iLCJST0xFX1BJQ0tMSVNUX1BSSU9SSVRJWkUiLCJST0xFX1NISVBNRU5UX1JFQUQiLCJST0xFX1NISVBNRU5UX1BSSU5UIiwiUk9MRV9TSElQTUVOVF9ET1dOTE9BRCIsIlJPTEVfU0hJUE1FTlRfRVhQT1JUIiwiUk9MRV9NQUlMU0hJUE1FTlRfUkVBRCIsIlJPTEVfTUFJTFNISVBNRU5UX1VQREFURSIsIlJPTEVfTUFJTFNISVBNRU5UX1BST0NFU1MiLCJST0xFX1RSQUNLSU5HREFUQV9SRUFEIiwiUk9MRV9UUkFDS0lOR0RBVEFfVVBEQVRFIiwiUk9MRV9UUkFDS0lOR0RBVEFfREVMRVRFIiwiUk9MRV9SRVRVUk5MQUJFTF9SRUFEIiwiUk9MRV9SRVRVUk5MQUJFTF9DUkVBVEUiLCJST0xFX1JFVFVSTkxBQkVMX1VQREFURSIsIlJPTEVfUkVUVVJOTEFCRUxfQ0FOQ0VMIiwiUk9MRV9QUklOVEVSX1JFQUQiLCJST0xFX1BSSU5URVJfVVBEQVRFIiwiUk9MRV9QUklOVEVSX0NSRUFURSIsIlJPTEVfUFJJTlRFUl9ERUxFVEUiLCJST0xFX1BBQ0tJTkdUQUJMRV9SRUFEIiwiUk9MRV9QQUNLSU5HVEFCTEVfQ1JFQVRFIiwiUk9MRV9QQUNLSU5HVEFCTEVfREVMRVRFIiwiUk9MRV9QQUNLSU5HVEFCTEVfVVBEQVRFIiwiUk9MRV9QQUNLSU5HVEFCTEVfVVBEQVRFX0FERFJFU1MiLCJST0xFX1BBQ0tJTkdUQUJMRV9VUERBVEVfU0hJUFBJTkdPUFRJT04iLCJST0xFX0ZJTExJTkdfUkVBRCIsIlJPTEVfRklMTElOR19FWFBPUlQiLCJST0xFX0ZJTExJTkdfSU1QT1JUIiwiUk9MRV9DT0xMT19SRUFEIiwiUk9MRV9DT0xMT19FWFBPUlQiLCJST0xFX0NPTExPX0lNUE9SVCIsIlJPTEVfQ1VTVE9NRVJfUkVBRCIsIlJPTEVfQ1VTVE9NRVJfQ1JFQVRFIiwiUk9MRV9DVVNUT01FUl9VUERBVEUiLCJST0xFX0NVU1RPTUVSX0lNUE9SVCIsIlJPTEVfQ1VTVE9NRVJfRVhQT1JUIiwiUk9MRV9DVVNUT01FUl9ERUxFVEUiLCJST0xFX0NVU1RPTUVSVVNFUl9SRUFEIiwiUk9MRV9DVVNUT01FUlVTRVJfQ1JFQVRFIiwiUk9MRV9DVVNUT01FUlVTRVJfVVBEQVRFIiwiUk9MRV9DVVNUT01FUlVTRVJfREVMRVRFIiwiUk9MRV9DVVNUT01FUlVTRVJfRVhQT1JUIiwiUk9MRV9DVVNUT01FUlVTRVJfSU1QT1JUIiwiUk9MRV9DVVNUT01FUkdST1VQX1JFQUQiLCJST0xFX0NVU1RPTUVSR1JPVVBfQ1JFQVRFIiwiUk9MRV9DVVNUT01FUkdST1VQX1VQREFURSIsIlJPTEVfQ1VTVE9NRVJHUk9VUF9ERUxFVEUiLCJST0xFX0FQSV9SRUFEIiwiUk9MRV9BUElfQ1JFQVRFIiwiUk9MRV9BUElfVVBEQVRFIiwiUk9MRV9BUElfREVMRVRFIiwiUk9MRV9SRVNUUklDVEVESVBfUkVBRCIsIlJPTEVfUkVTVFJJQ1RFRElQX1VQREFURSIsIlJPTEVfUkVTVFJJQ1RFRElQX0RFTEVURSIsIlJPTEVfRU1QTE9ZRUVfUkVBRCIsIlJPTEVfRU1QTE9ZRUVfQ1JFQVRFIiwiUk9MRV9FTVBMT1lFRV9VUERBVEUiLCJST0xFX0VNUExPWUVFX0RFTEVURSIsIlJPTEVfRU1QTE9ZRUVfRVhQT1JUIiwiUk9MRV9FTVBMT1lFRV9JTVBPUlQiLCJST0xFX0VNUExPWUVFR1JPVVBfUkVBRCIsIlJPTEVfRU1QTE9ZRUVHUk9VUF9DUkVBVEUiLCJST0xFX0VNUExPWUVFR1JPVVBfVVBEQVRFIiwiUk9MRV9FTVBMT1lFRUdST1VQX0RFTEVURSIsIlJPTEVfTE9DQVRJT05fUkVBRCIsIlJPTEVfTE9DQVRJT05fQ1JFQVRFIiwiUk9MRV9MT0NBVElPTl9VUERBVEUiLCJST0xFX0xPQ0FUSU9OX0RFTEVURSIsIlJPTEVfTE9DQVRJT05fSU1QT1JUIiwiUk9MRV9MT0NBVElPTl9FWFBPUlQiLCJST0xFX0xPQ0FUSU9OX1FVQVJBTlRJTkUiLCJST0xFX0xPQ0FUSU9OR1JPVVBfUkVBRCIsIlJPTEVfTE9DQVRJT05HUk9VUF9DUkVBVEUiLCJST0xFX0xPQ0FUSU9OR1JPVVBfVVBEQVRFIiwiUk9MRV9MT0NBVElPTkdST1VQX0RFTEVURSIsIlJPTEVfV0FSRUhPVVNFU19SRUFEIiwiUk9MRV9aT05FX1JFQUQiLCJST0xFX1pPTkVfQ1JFQVRFIiwiUk9MRV9aT05FX1VQREFURSIsIlJPTEVfWk9ORV9ERUxFVEUiLCJST0xFX1pPTkVfRVhQT1JUIiwiUk9MRV9aT05FX0lNUE9SVCIsIlJPTEVfUFJJTlRfQkFSQ09ERSIsIlJPTEVfU0hJUFBJTkdNQVRSSVhfUkVBRCIsIlJPTEVfU0hJUFBJTkdNQVRSSVhfVVBEQVRFIiwiUk9MRV9CVVNJTkVTU1JVTEVNQVRSSVhfUkVBRCIsIlJPTEVfQlVTSU5FU1NSVUxFTUFUUklYX1VQREFURSIsIlJPTEVfU0hJUFBJTkdNRVRIT0RfUkVBRCIsIlJPTEVfU0hJUFBJTkdNRVRIT0RfQ1JFQVRFIiwiUk9MRV9TSElQUElOR01FVEhPRF9VUERBVEUiLCJST0xFX0VYUE9SVF9SRUFEX0ZJTkFOQ0lBTCIsIlJPTEVfRVhQT1JUX1JFQURfQklMTElORyIsIlJPTEVfSVNTVUVfUkVBRCIsIlJPTEVfSVNTVUVfQVNTSUdOIiwiUk9MRV9JU1NVRV9DUkVBVEVfQ09NTUVOVCIsIlJPTEVfSVNTVUVfUkVBRF9DT01NRU5UIiwiUk9MRV9TSElQUElOR1RFTVBMQVRFX1JFQUQiLCJST0xFX1NISVBQSU5HVEVNUExBVEVfVVBEQVRFIiwiUk9MRV9DT05UUkFDVF9SRUFEIiwiUk9MRV9DT05UUkFDVF9DUkVBVEUiLCJST0xFX0NPTlRSQUNUX1VQREFURSIsIlJPTEVfQ1VTVE9NRVJQUklDRV9SRUFEIiwiUk9MRV9DVVNUT01FUlBSSUNFX1VQREFURSIsIlJPTEVfU0VSSUFMTlVNQkVSX1JFQUQiLCJST0xFX1NFUklBTE5VTUJFUl9FWFBPUlQiLCJST0xFX1NISVBQSU5HU09GVFdBUkVfUkVBRCIsIlJPTEVfU0hJUFBJTkdTT0ZUV0FSRV9FWFBPUlQiLCJST0xFX01JRERMRVdBUkVfUkVBRCIsIlJPTEVfSU5TVFJVQ1RJT05TX09WRVJWSUVXX1JFQUQiLCJST0xFX0lOU1RSVUNUSU9OU19ET1dOTE9BRF9BUEtfUkVBRCIsIlJPTEVfSU5TVFJVQ1RJT05TX1NFTEVDVF9XTVNfQVBQX1JFQUQiLCJST0xFX1dFQiIsIlJPTEVfVVNFUiJdLCJ1c2VybmFtZSI6ImZlcnJ5IiwidXNlcl9pZCI6IjlmZDNlZmYwLWZiMjgtMTFlNS05YzMyLWJjNWZmNGY3YWVmNCIsInVzZXJfdHlwZSI6ImVtcGxveWVlIiwiY3VzdG9tZXJfaWRzIjpbIjUzYjVhNTQzLTEyOWEtNDAzYy05YTZlLTNkOWM1MjVmZmE1YiIsImYxOTA5MDBhLWViZmQtNDI2Mi05ZGQ2LTA1ZGRkNjE3MjFiMCIsIjhjZTEwNWYwLWZjMWQtNDIzYS1iMDY2LWQ4NGM1ZWE1N2NhYSIsIjQ4ZTc3YTdhLWUwMzMtNDcxOS05MTkxLTc4YTlhMWI0NjQ5MiJdLCJyZXF1ZXN0X2lwIjoiMTkyLjE2OC4xMjguMSJ9.crcZ-2i9u1u5i3RBhV6tCMo-hrdeuQ91yDDVGT9k6iAFbF48k65RQbVPVkrIwZx9wN6hCvl6mMOOGkiLxFtweSi4nt_hGZeCsuieypQHZxf3MCdwo0zKtb0M8NmBB--D7_AvHWqcz6IEgoXMUtYLOkab4BPVdZlHmegbf7qRtNZlaKRVXPqgn3ReiPVvX_TGdK74VEXZzWPStoTxJwVkFvCFV9RFfYb_b9BgfTaSDJAYGFmSE-QxbW1K4TQBgUjuUAQSRh-y5diw4nuY9VJgcJ2LAD6ZX19do1zFCsc8zq2KUoTppPV9xO8WpOdxlXKGLu3rwfvLV9clhrc9ogmEAYF7UDcJkwgL5nHEfmsAD602T6_NtMjwP1dhTL9OeRz6oJwNRUb3hSe6uG7hvhlE7X-O8GwCafyWX8vgGT0D1NPh5ehwFsh8oc57M-W5PczDwZwQJ99jdHcAFRcsEKMJpKrs1G2LYAqDMS38i6IbZghPqN88Cnc6cpPfWVI6rs1BPZ4DxRBkQkXLWdamAVck6mCpW1QOA-YnNbmLn16d88PeMhzt7TN_jJfi0VAf2BK1DEbdy2sdSoqm3kCWqSzG11hTDLjvbpvJ0rCby7kz4c47qyxzxhyYOCBD4Rns9bNRW2xbE4BSJ0eKMeacaaWNQX0LeUaQy2Q6qPCVPO-hxAo"
    assert client.refresh_token == "91aff30e4f3bb35b923892e525bd848ab88cf68d9669b5ccf07ae0262934b43a67cf7df89ef6213ddbb47c400c1b2c32e4d9178790caa1420e28a94b892addb3"

    # Expired JWT triggering refresh of auth
    client.order.list()

    # Auth after refresh
    assert client.access_token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2Mzg1NDgyNTAsImV4cCI6MTYzODU1MTg1MCwicm9sZXMiOlsiUk9MRV9TQ0FOTkVSIiwiUk9MRV9EQVNIQk9BUkRfUkVBRCIsIlJPTEVfREFTSEJPQVJEX1NUQVRVUyIsIlJPTEVfU1RPQ0tfUkVBRCIsIlJPTEVfU1RPQ0tfSU1QT1JUIiwiUk9MRV9TVE9DS19FWFBPUlQiLCJST0xFX1NUT0NLSElTVE9SWV9SRUFEIiwiUk9MRV9TVE9DS0hJU1RPUllfRVhQT1JUIiwiUk9MRV9NT0RJRklDQVRJT05fUkVBRCIsIlJPTEVfTU9ESUZJQ0FUSU9OX0NSRUFURSIsIlJPTEVfTU9ESUZJQ0FUSU9OX1VQREFURSIsIlJPTEVfTU9ESUZJQ0FUSU9OX0FQUFJPVkUiLCJST0xFX01PRElGSUNBVElPTl9FWFBPUlQiLCJST0xFX1RSQU5TRkVSX1JFQUQiLCJST0xFX1RSQU5TRkVSX0NSRUFURSIsIlJPTEVfVFJBTlNGRVJfVVBEQVRFIiwiUk9MRV9UUkFOU0ZFUl9ERUxFVEUiLCJST0xFX1RSQU5TRkVSX0NBTkNFTCIsIlJPTEVfVFJBTlNGRVJfVU5IT0xEIiwiUk9MRV9UUkFOU0ZFUl9VTkFTU0lHTiIsIlJPTEVfVFJBTlNGRVJfUkVWSUVXIiwiUk9MRV9UUkFOU0ZFUl9FWFBPUlQiLCJST0xFX0FSVElDTEVfUkVBRCIsIlJPTEVfQVJUSUNMRV9DUkVBVEUiLCJST0xFX0FSVElDTEVfVVBEQVRFX0JBUkNPREVTIiwiUk9MRV9BUlRJQ0xFX1VQREFURSIsIlJPTEVfQVJUSUNMRV9ERUxFVEUiLCJST0xFX0FSVElDTEVfSU1QT1JUIiwiUk9MRV9BUlRJQ0xFX1VQREFURV9ET0NVTUVOVFMiLCJST0xFX0FSVElDTEVfRVhQT1JUIiwiUk9MRV9WQVJJQU5UX1FVQVJBTlRJTkUiLCJST0xFX1NVUFBMSUVSX1JFQUQiLCJST0xFX1NVUFBMSUVSX0NSRUFURSIsIlJPTEVfU1VQUExJRVJfVVBEQVRFIiwiUk9MRV9TVVBQTElFUl9ERUxFVEUiLCJST0xFX0lOQk9VTkRfUkVBRCIsIlJPTEVfSU5CT1VORF9DUkVBVEUiLCJST0xFX0lOQk9VTkRfVVBEQVRFIiwiUk9MRV9JTkJPVU5EX0NBTkNFTCIsIlJPTEVfSU5CT1VORF9QUk9DRVNTIiwiUk9MRV9JTkJPVU5EX0NPTVBMRVRFIiwiUk9MRV9JTkJPVU5EX0VYUE9SVCIsIlJPTEVfT1JERVJfUkVBRCIsIlJPTEVfT1JERVJfQ1JFQVRFIiwiUk9MRV9PUkRFUl9VUERBVEUiLCJST0xFX09SREVSX1VQREFURV9QUk9DRVNTSU5HIiwiUk9MRV9PUkRFUl9VUERBVEVfUEFBWkwiLCJST0xFX09SREVSX1BBUlRJQUwiLCJST0xFX09SREVSX1VOSE9MRCIsIlJPTEVfT1JERVJfQ0FOQ0VMIiwiUk9MRV9PUkRFUl9DQU5DRUxfUFJPQ0VTU0lORyIsIlJPTEVfT1JERVJfUFJPQkxFTSIsIlJPTEVfT1JERVJfRVhQT1JUIiwiUk9MRV9PUkRFUl9QUklPUklUSVpFIiwiUk9MRV9PUkRFUl9JTVBPUlQiLCJST0xFX1BJQ0tMSVNUX1JFQUQiLCJST0xFX1BJQ0tMSVNUX0VYUE9SVCIsIlJPTEVfUElDS0xJU1RfVU5BU1NJR04iLCJST0xFX1BJQ0tMSVNUX1BSSU9SSVRJWkUiLCJST0xFX1NISVBNRU5UX1JFQUQiLCJST0xFX1NISVBNRU5UX1BSSU5UIiwiUk9MRV9TSElQTUVOVF9ET1dOTE9BRCIsIlJPTEVfU0hJUE1FTlRfRVhQT1JUIiwiUk9MRV9NQUlMU0hJUE1FTlRfUkVBRCIsIlJPTEVfTUFJTFNISVBNRU5UX1VQREFURSIsIlJPTEVfTUFJTFNISVBNRU5UX1BST0NFU1MiLCJST0xFX1RSQUNLSU5HREFUQV9SRUFEIiwiUk9MRV9UUkFDS0lOR0RBVEFfVVBEQVRFIiwiUk9MRV9UUkFDS0lOR0RBVEFfREVMRVRFIiwiUk9MRV9SRVRVUk5MQUJFTF9SRUFEIiwiUk9MRV9SRVRVUk5MQUJFTF9DUkVBVEUiLCJST0xFX1JFVFVSTkxBQkVMX1VQREFURSIsIlJPTEVfUkVUVVJOTEFCRUxfQ0FOQ0VMIiwiUk9MRV9QUklOVEVSX1JFQUQiLCJST0xFX1BSSU5URVJfVVBEQVRFIiwiUk9MRV9QUklOVEVSX0NSRUFURSIsIlJPTEVfUFJJTlRFUl9ERUxFVEUiLCJST0xFX1BBQ0tJTkdUQUJMRV9SRUFEIiwiUk9MRV9QQUNLSU5HVEFCTEVfQ1JFQVRFIiwiUk9MRV9QQUNLSU5HVEFCTEVfREVMRVRFIiwiUk9MRV9QQUNLSU5HVEFCTEVfVVBEQVRFIiwiUk9MRV9QQUNLSU5HVEFCTEVfVVBEQVRFX0FERFJFU1MiLCJST0xFX1BBQ0tJTkdUQUJMRV9VUERBVEVfU0hJUFBJTkdPUFRJT04iLCJST0xFX0ZJTExJTkdfUkVBRCIsIlJPTEVfRklMTElOR19FWFBPUlQiLCJST0xFX0ZJTExJTkdfSU1QT1JUIiwiUk9MRV9DT0xMT19SRUFEIiwiUk9MRV9DT0xMT19FWFBPUlQiLCJST0xFX0NPTExPX0lNUE9SVCIsIlJPTEVfQ1VTVE9NRVJfUkVBRCIsIlJPTEVfQ1VTVE9NRVJfQ1JFQVRFIiwiUk9MRV9DVVNUT01FUl9VUERBVEUiLCJST0xFX0NVU1RPTUVSX0lNUE9SVCIsIlJPTEVfQ1VTVE9NRVJfRVhQT1JUIiwiUk9MRV9DVVNUT01FUl9ERUxFVEUiLCJST0xFX0NVU1RPTUVSVVNFUl9SRUFEIiwiUk9MRV9DVVNUT01FUlVTRVJfQ1JFQVRFIiwiUk9MRV9DVVNUT01FUlVTRVJfVVBEQVRFIiwiUk9MRV9DVVNUT01FUlVTRVJfREVMRVRFIiwiUk9MRV9DVVNUT01FUlVTRVJfRVhQT1JUIiwiUk9MRV9DVVNUT01FUlVTRVJfSU1QT1JUIiwiUk9MRV9DVVNUT01FUkdST1VQX1JFQUQiLCJST0xFX0NVU1RPTUVSR1JPVVBfQ1JFQVRFIiwiUk9MRV9DVVNUT01FUkdST1VQX1VQREFURSIsIlJPTEVfQ1VTVE9NRVJHUk9VUF9ERUxFVEUiLCJST0xFX0FQSV9SRUFEIiwiUk9MRV9BUElfQ1JFQVRFIiwiUk9MRV9BUElfVVBEQVRFIiwiUk9MRV9BUElfREVMRVRFIiwiUk9MRV9SRVNUUklDVEVESVBfUkVBRCIsIlJPTEVfUkVTVFJJQ1RFRElQX1VQREFURSIsIlJPTEVfUkVTVFJJQ1RFRElQX0RFTEVURSIsIlJPTEVfRU1QTE9ZRUVfUkVBRCIsIlJPTEVfRU1QTE9ZRUVfQ1JFQVRFIiwiUk9MRV9FTVBMT1lFRV9VUERBVEUiLCJST0xFX0VNUExPWUVFX0RFTEVURSIsIlJPTEVfRU1QTE9ZRUVfRVhQT1JUIiwiUk9MRV9FTVBMT1lFRV9JTVBPUlQiLCJST0xFX0VNUExPWUVFR1JPVVBfUkVBRCIsIlJPTEVfRU1QTE9ZRUVHUk9VUF9DUkVBVEUiLCJST0xFX0VNUExPWUVFR1JPVVBfVVBEQVRFIiwiUk9MRV9FTVBMT1lFRUdST1VQX0RFTEVURSIsIlJPTEVfTE9DQVRJT05fUkVBRCIsIlJPTEVfTE9DQVRJT05fQ1JFQVRFIiwiUk9MRV9MT0NBVElPTl9VUERBVEUiLCJST0xFX0xPQ0FUSU9OX0RFTEVURSIsIlJPTEVfTE9DQVRJT05fSU1QT1JUIiwiUk9MRV9MT0NBVElPTl9FWFBPUlQiLCJST0xFX0xPQ0FUSU9OX1FVQVJBTlRJTkUiLCJST0xFX0xPQ0FUSU9OR1JPVVBfUkVBRCIsIlJPTEVfTE9DQVRJT05HUk9VUF9DUkVBVEUiLCJST0xFX0xPQ0FUSU9OR1JPVVBfVVBEQVRFIiwiUk9MRV9MT0NBVElPTkdST1VQX0RFTEVURSIsIlJPTEVfV0FSRUhPVVNFU19SRUFEIiwiUk9MRV9aT05FX1JFQUQiLCJST0xFX1pPTkVfQ1JFQVRFIiwiUk9MRV9aT05FX1VQREFURSIsIlJPTEVfWk9ORV9ERUxFVEUiLCJST0xFX1pPTkVfRVhQT1JUIiwiUk9MRV9aT05FX0lNUE9SVCIsIlJPTEVfUFJJTlRfQkFSQ09ERSIsIlJPTEVfU0hJUFBJTkdNQVRSSVhfUkVBRCIsIlJPTEVfU0hJUFBJTkdNQVRSSVhfVVBEQVRFIiwiUk9MRV9CVVNJTkVTU1JVTEVNQVRSSVhfUkVBRCIsIlJPTEVfQlVTSU5FU1NSVUxFTUFUUklYX1VQREFURSIsIlJPTEVfU0hJUFBJTkdNRVRIT0RfUkVBRCIsIlJPTEVfU0hJUFBJTkdNRVRIT0RfQ1JFQVRFIiwiUk9MRV9TSElQUElOR01FVEhPRF9VUERBVEUiLCJST0xFX0VYUE9SVF9SRUFEX0ZJTkFOQ0lBTCIsIlJPTEVfRVhQT1JUX1JFQURfQklMTElORyIsIlJPTEVfSVNTVUVfUkVBRCIsIlJPTEVfSVNTVUVfQVNTSUdOIiwiUk9MRV9JU1NVRV9DUkVBVEVfQ09NTUVOVCIsIlJPTEVfSVNTVUVfUkVBRF9DT01NRU5UIiwiUk9MRV9TSElQUElOR1RFTVBMQVRFX1JFQUQiLCJST0xFX1NISVBQSU5HVEVNUExBVEVfVVBEQVRFIiwiUk9MRV9DT05UUkFDVF9SRUFEIiwiUk9MRV9DT05UUkFDVF9DUkVBVEUiLCJST0xFX0NPTlRSQUNUX1VQREFURSIsIlJPTEVfQ1VTVE9NRVJQUklDRV9SRUFEIiwiUk9MRV9DVVNUT01FUlBSSUNFX1VQREFURSIsIlJPTEVfU0VSSUFMTlVNQkVSX1JFQUQiLCJST0xFX1NFUklBTE5VTUJFUl9FWFBPUlQiLCJST0xFX1NISVBQSU5HU09GVFdBUkVfUkVBRCIsIlJPTEVfU0hJUFBJTkdTT0ZUV0FSRV9FWFBPUlQiLCJST0xFX01JRERMRVdBUkVfUkVBRCIsIlJPTEVfSU5TVFJVQ1RJT05TX09WRVJWSUVXX1JFQUQiLCJST0xFX0lOU1RSVUNUSU9OU19ET1dOTE9BRF9BUEtfUkVBRCIsIlJPTEVfSU5TVFJVQ1RJT05TX1NFTEVDVF9XTVNfQVBQX1JFQUQiLCJST0xFX1dFQiIsIlJPTEVfVVNFUiJdLCJ1c2VybmFtZSI6ImZlcnJ5IiwidXNlcl9pZCI6IjlmZDNlZmYwLWZiMjgtMTFlNS05YzMyLWJjNWZmNGY3YWVmNCIsInVzZXJfdHlwZSI6ImVtcGxveWVlIiwiY3VzdG9tZXJfaWRzIjpbIjUzYjVhNTQzLTEyOWEtNDAzYy05YTZlLTNkOWM1MjVmZmE1YiIsImYxOTA5MDBhLWViZmQtNDI2Mi05ZGQ2LTA1ZGRkNjE3MjFiMCIsIjhjZTEwNWYwLWZjMWQtNDIzYS1iMDY2LWQ4NGM1ZWE1N2NhYSIsIjQ4ZTc3YTdhLWUwMzMtNDcxOS05MTkxLTc4YTlhMWI0NjQ5MiJdLCJyZXF1ZXN0X2lwIjoiMTkyLjE2OC4xMjguMSJ9.PnAIQCRUARfBqM31W41bgeheayxpwhL1e9IT3ytH-WL8DNlYkS2n_ydUtRxFHE2rK7Av5Qo1xTg4OMrpjMcBKPCcU2ZzvJTi6525ON6LoIJW-jJAGAYT3cw7yPYSr5f3xuOrS5ZA8uOjy2o8TEne7jlAAQhBBmj2fa5js28tcORBaO7Vwn4sAnHaThlmcopjbefLuK1TUSwQ88ky-8xBYF1L53v6oyWuFqGJvOOCwH51hl7AchbOP_xshZiAFV6wmBdx90DEVFDLsL3hxZxd-cqFGDDAZYmvPjX0154BoHSKNDJssftgCJuWXcfNo-p5dL-Bq-b55NklZOIii2qcvcMV3UTMuQsOzBOzmigk5gOl2nnEwwVOmBQUKEFqLxaLhY6vOEMZofq9Q2jUwudR6DtPLiJpuZCODNr77eL3hiF_hAi42WzMmUxg4y-K3CifuN2AT2-c7Hd9tA2JSpDL_yrtCSo8ZstzXvNzIMlcjsX9NSslEhPh2sY8HQlqhjac0ZUqwve1_U1PUjs1B6-66fNsRQYPuYzc-d3w4gHHB_l0ml2UibmLr8QujrlTji5i8sNPMq8k0TJ1KiWtxoMW3UJ0ZgD3npl1WmrkHBI71WzL35qxDmEP-YiBtuJBDe7lTZw1jgrNkDYE7IHEitT4-16puxyHw4n4jUlmgiPi-u0"
    assert client.refresh_token == "405b4e2c9e8659f3f5c20b0574564cb9365c65a6f9561f310d57af391a538f627bb490d96f11d5caa6cfe27c1b9753403536ac30e7307094b1aba5d2a50db2ec"


def test_invalid_auth(client, response):
    assert client.access_token is None
    assert client.refresh_token is None
    assert client.expires_at is 0

    response.post("https://api.ewarehousing.com/api/wms/auth/login", "auth_login_error", status=401)

    with pytest.raises(AuthenticationError):
        client.order.list()
