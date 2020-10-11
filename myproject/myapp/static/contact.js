$(function () {

    // init the validator
    // validator files are included in the download package
    // otherwise download from http://1000hz.github.io/bootstrap-validator

    $('#contact-form').validator();

    // when the form is submitted
    $('#send').on('click', function (e) {

        $('#responseAreaImage').css("display", "block");
        $('#responseArea').css("display", "none");
        $('#showCheckBox').css("display","block")
        // if the validator does not prevent form submit
        if (!e.isDefaultPrevented()) {
            var form = $("#contact-form");

            // POST values in the background the the script URL
            //fetch using a Request and a Headers objects
            var url='';
            ip=$("#ip_address").val()
            email=$("#form_Email").val()
            org_name=$("#form_org_name").val()
            key=$("#form_key").val()
            Requested_Amount=$("#form_Requested_Amount").val()
            Emi_Amount=$("#form_Emi_Amount").val()
            Age=$("#form_Age").val()
            Ex_Showroom_Price=$("#form_Ex_Showroom_Price").val()
            Cost_Of_Vehicle=$("#form_Cost_Of_Vehicle").val()
            Loan_Term=$("#form_Loan_Term").val()
            
            cibil_score=$("#form_cibil_score").val()
            No_Of_Years_At_Residence=$("#form_No_Of_Years_At_Residence").val()
            No_Of_Years_In_City=$("#form_No_Of_Years_In_City").val()
            year=$("#form_year").val()
            Segment=$("#form_Segment").val()
            Gender=$("#form_Gender").val()
            max_loan_term_in_months=$("#form_max_loan_term_in_months").val()
            country_status=$("#country_status").val()
            approvedIRR=$('#approvedIRR').val()
            if($('#saveToDb').prop("checked"))
             saveToDb=1
             else
             saveToDb=0


           // alert(ip)

            const xhr = new XMLHttpRequest();
            url = ip+'/?email='+email+'&org_name='+org_name+'&key='+key+'&Requested_Amount='+Requested_Amount
            +'&Emi_Amount='+Emi_Amount+'&Age='+Age+'&Ex_Showroom_Price='+Ex_Showroom_Price+'&Cost_Of_Vehicle='+Cost_Of_Vehicle
            +'&Loan_Term='+Loan_Term+'&cibil_score='+cibil_score+'&No_Of_Years_At_Residence='+No_Of_Years_At_Residence+'&No_Of_Years_In_City='
            +No_Of_Years_In_City+'&year='+year+'&Segment='+Segment+'&Gender='+Gender+'&country_status='+country_status+'&max_loan_term_in_months='+max_loan_term_in_months+'&approvedIRR='+approvedIRR+'&saveToDb='+saveToDb;
           // alert(url)
            xhr.open('GET', url);
            
            xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            // defensive check
            if (typeof callback === "function") {
                // apply() sets the meaning of "this" in the callback
                callback.apply(xhr);

            }
            var result=(xhr.response)
            data=$.parseJSON(result);
            var fResponse='';
            $.each(data, function(i, item) {
                fResponse+='<div style="font-family:arial;color:red;font-style:italic">'+i+': '+item+'</div>';
            });
            $('#responseAreaImage').css("display", "none");
            $('#responseArea').html(fResponse)
            $('#responseArea').css("display", "block");
        }
        else
        {
            $('#responseAreaImage').css("display", "none");
            $('#responseArea').html('Try to Reload the Page...')
            $('#responseArea').css("display", "block");
        }
    };
            xhr.send(); 
            


        }else{
            return false;
        }
        
    })
});

function executeForm(e)
{
    $('#contact-form').validator();
    if (!e.isDefaultPrevented()) {
        //var url = var url = "ml/";
        var form = $("#contact-form");
        const xhr = new XMLHttpRequest();
        const url = 'http://127.0.0.1:8000/mlProcess/?email=shareif%40test.com&org_name=ASWT&key=gsScFk_4STB4dck6ArtjVw&Requested_Amount=10000&Emi_Amount=255&Age=35&Ex_Showroom_Price=100000&Cost_Of_Vehicle=10000&Loan_Term=36&cibil_score=5&No_Of_Years_At_Residence=4&No_Of_Years_In_City=4&year=2020&Segment=SUV&Gender=Male&max_loan_term_in_months=200';
       // alert(url)
        xhr.open('GET', url);
        xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
        // defensive check
        if (typeof callback === "function") {
            // apply() sets the meaning of "this" in the callback
            callback.apply(xhr);

        }
        alert(xhr.response)
    }
};
        xhr.send(); 
        


    }else{
        return false;
    }
}