from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from fpdf import FPDF

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1M_FWpbVSf2mRdJhIRDFUk1GkNYCL42VIbdTegOwQ6_U'
SAMPLE_RANGE_NAME = 'A:AA'

pdf = FPDF()

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    pdf.add_page(orientation='L')
    pdf.set_font("Helvetica", size=5)

    nodes = 0

    clusters = values[0][1:]
    
    total_clusters = 0
    cluster_count = 0

    cp_components = ['ADB', 'C3', 'KSQLDB', 'CONNECT', 'SR', 'REST', 'BROKER', 'ZK', 'REPLICATOR', 'MQTT', 'STREAMS', 'OPERATOR']

    if not values:
        print('No data found.')
    else:
        for cluster in clusters:
            pdf.set_xy(15 + (cluster_count%2 * 100), 15 + (int(cluster_count/2) * 150))
            
            pdf.cell(80, 174, "", 1, 2, 'L')
            pdf.text(pdf.get_x() + 5, pdf.get_y() - 169, cluster)

            for i in range(1, len(values)):
                row = values[i]

                for icons in range(0, int(row[total_clusters+1])):
                    pdf.set_xy(22.5 + (cluster_count%2 * 100) + (nodes%3 * 25), 25 + (int(cluster_count/2) * 150) + (int(nodes/3) * 30))

                    pdf.cell(10, 10, "", 1, 2, 'L')
                    pdf.text(pdf.get_x() + 2, pdf.get_y() + 2, row[0])

                    if row[0] in cp_components:
                        cp_component = 'cp_components/' + str(row[0]) + '.png'
                        pdf.image(cp_component, x=pdf.get_x() + 0.5, y=pdf.get_y() - 9, w=7.5)

                    nodes = nodes + 1

            nodes = 0
            cluster_count = cluster_count + 1
            total_clusters = total_clusters + 1

            if cluster_count%2 == 0:
                pdf.add_page(orientation='L')
                pdf.set_xy(0, 0)
                cluster_count = 0

    pdf.output("confluent_topology.pdf")

if __name__ == '__main__':
    main()