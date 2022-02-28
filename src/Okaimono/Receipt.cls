Class Okaimono.Receipt Extends %Persistent
{

Property StoreName As %String;

Property OkaimonoDateTime As %TimeStamp;

Property TotalPrice As %Numeric;

Property Discount As %Numeric;

/// 購入商品詳細（多側）リレーションシッププロパティとして定義
Relationship Items As Okaimono.Item [ Cardinality = many, Inverse = Receipt ];

Storage Default
{
<Data name="ReceiptDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>StoreName</Value>
</Value>
<Value name="3">
<Value>OkaimonoDateTime</Value>
</Value>
<Value name="4">
<Value>TotalPrice</Value>
</Value>
<Value name="5">
<Value>Discount</Value>
</Value>
</Data>
<DataLocation>^Okaimono.ReceiptD</DataLocation>
<DefaultData>ReceiptDefaultData</DefaultData>
<IdLocation>^Okaimono.ReceiptD</IdLocation>
<IndexLocation>^Okaimono.ReceiptI</IndexLocation>
<StreamLocation>^Okaimono.ReceiptS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
