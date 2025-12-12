from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from VsyPy20022.fi_to_fi_pacs008.pacs00800108.pacs_008_001_08 import *

def testGeneratePacs008():

    # Iniassisi object pacs.008
    myPacs008 = Document()

    # Inissiasi FiToFiCustomerCreditTransferV08
    myPacs008.fito_ficstmr_cdt_trf = FitoFicustomerCreditTransferV08()

    # Inisaisi credit transfer transaction informasi
    myPacs008.fito_ficstmr_cdt_trf.cdt_trf_tx_inf = list()

    ## Create creditor
    data = CreditTransferTransaction39()
    data.cdtr_acct = CashAccount38()
    data.cdtr_acct.id = AccountIdentification4Choice()
    data.cdtr_acct.id.othr = GenericAccountIdentification1()
    data.cdtr_acct.id.othr.id = '55872546987'


    data.cdtr = PartyIdentification135()
    data.cdtr.nm = "Nu'man Noah"
    data.cdtr.pstl_adr = PostalAddress24()
    data.cdtr.pstl_adr.ctry = "MY"
    data.cdtr.pstl_adr.twn_nm = "Selangor"
    data.cdtr.pstl_adr.bldg_nb = '25'

    ## Create debtor
    data.dbtr = PartyIdentification135()
    data.dbtr.nm = "Muhammad Farras Ma'ruf"
    data.dbtr.pstl_adr = PostalAddress24()
    data.dbtr.pstl_adr.ctry = "ID"
    data.dbtr.pstl_adr.twn_nm = "Bandung"
    data.dbtr.pstl_adr.adr_line.append("jalan bandung raya kabupaten cimengka")

    # Input the message
    # Add to the list of credittrasnfer taranscstions
    myPacs008.fito_ficstmr_cdt_trf.cdt_trf_tx_inf.append(data)


    return myPacs008


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Call the object
    objectPacs008 = testGeneratePacs008()

    config = SerializerConfig(indent="  ")
    context = XmlContext()
    serializer = XmlSerializer(context=context, config=config)

    print(serializer.render(objectPacs008,ns_map={None: "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08"}))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
