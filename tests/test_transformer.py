import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from transformer import Transformer

def test_parse_to_dataframe():
    xml = """
    <root xmlns="urn:iso:std:iso:20022:tech:xsd:auth.036.001.02">
        <FinInstrm>
            <ModfdRcrd>
                <FinInstrmGnlAttrbts>
                    <Id>ID123</Id>
                    <FullNm>Test Name</FullNm>
                    <ClssfctnTp>ABC</ClssfctnTp>
                    <CmmdtyDerivInd>false</CmmdtyDerivInd>
                    <NtnlCcy>EUR</NtnlCcy>
                </FinInstrmGnlAttrbts>
                <Issr>Issuer1</Issr>
            </ModfdRcrd>
        </FinInstrm>
    </root>
    """

    transformer = Transformer(xml)
    df = transformer.parse_to_dataframe()

    assert len(df) == 1
    assert df.iloc[0]["FinInstrmGnlAttrbts.Id"] == "ID123"
    assert df.iloc[0]["Issr"] == "Issuer1"

def test_add_a_count_and_contains_a():

    data = {
        "FinInstrmGnlAttrbts.FullNm": ["technical", "assessment", "steelEye", "", "abracadabra"]
    }

    df = pd.DataFrame(data)

    transformer = Transformer("")
    df = transformer.add_new_columns(df)

    assert df["a_count"].tolist() == [1, 1, 0, 0, 5]
    assert df["contains_a"].tolist() == ["YES", "YES", "NO", "NO", "YES"]