Class Okaimono.Item Extends %Persistent
{

Property Name As %String(MAXLEN = 100);

Property Price As %Numeric;

/// レシート（1側）を指し示すリレーションシッププロパティ
Relationship Receipt As Okaimono.Receipt [ Cardinality = one, Inverse = Items ];

/// 多側クラスでは、リレーションシッププロパティに対してインデックスを付与しておきます
Index ReceiptIdx On Receipt;

Storage Default
{
<Data name="ItemDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Name</Value>
</Value>
<Value name="3">
<Value>Price</Value>
</Value>
<Value name="4">
<Value>Receipt</Value>
</Value>
</Data>
<DataLocation>^Okaimono.ItemD</DataLocation>
<DefaultData>ItemDefaultData</DefaultData>
<IdLocation>^Okaimono.ItemD</IdLocation>
<IndexLocation>^Okaimono.ItemI</IndexLocation>
<StreamLocation>^Okaimono.ItemS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
