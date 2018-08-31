DEST="/QIBM/UserData/WebSphere/AppServer/V7/Express/profiles/OWFINANCE/installedApps/OWFSYS_OWFINANCE/OPMCsi.ear/OwfWs.war/WEB-INF/lib"

for file in *
do
    if [ $file != ${0##*/} ]
    then
        pre=${file%-*.*.*.*}
        if [ -e "$DEST"/$file -a ${file%-*.*.*SNAPSHOT*.*} != $pre ]
        then
            echo "$DEST"/$file esiste
        else
            if [ -a "$DEST"/$pre* ]
            then
                echo rimuovo "$DEST"/$pre*
                rm -f "$DEST"/$pre*
            fi
            echo copio $file "$DEST"
            cp -f $file "$DEST"
        fi
    fi
done

