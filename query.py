select_ora = ("""select
'A' || to_char(t1.ANO_AUTORIZ) || '-' || to_char(t1.NUM_SEQ_AUTORIZ) codigo,
'A' || to_char(t1.ANO_AUTORIZ) || '-' || to_char(t1.NUM_SEQ_AUTORIZ) || '' || b.anxnumseq || '' ||  lower(replace(replace(translate(upper(trim(b.ANXDESNOMEARQ)),'ÁÂÃÄÀÉÊËÈÇÍÏÌÎÓÔÕÖÒÚÜÙÛ','AAAAAEEEECIIIIOOOOOUUUU'),chr(10),''),chr(13),chr(249))) arq_novo_nome,
b.ANXARQANEXO arquivo
--ATT_DATA_PROD.PACK_FUNCOES_DBA.clob_to_blob2(b.ANXARQANEXO) arquivo
from 
(
select distinct a.ANO_AUTORIZ, a.NUM_SEQ_AUTORIZ
from  DW_FSAS.dw_utilizacao_facplan_autoriz a
where 
not exists (
select t1.senha 
from 
(
select trim(xa.senha) senha from dw_fsas.dw_utilizacao_facplan_faturas xa 
union 
select trim(xb.num_senha_autoriz) senha from dw_fsas.dw_guias_facplan xb
) t1 where t1.senha = a.senha 
)
order by 1 desc,2 desc
) t1 join ATT_DATA_SCN.scttblanx b on (b.autano = t1.ano_autoriz and b.autnum = t1.num_seq_autoriz)
order by 1 desc
""")